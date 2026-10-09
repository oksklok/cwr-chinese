"""Focused reconstruction/restoration regressions; no commercial fixtures."""
import json
import signal
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import install_core as core
RECONSTRUCT = core.reconstruct
CONTENT_OUTPUTS = core.content_outputs
VERIFY_GAME = core.verify_game


class InstallCoreTests(unittest.TestCase):
    def test_version_checks_accept_compatible_x64_without_an_executable_hash(self):
        data = bytearray(72)
        data[:2] = b'MZ'
        core.struct.pack_into('<I', data, 60, 64)
        data[64:68] = b'PE\0\0'
        core.struct.pack_into('<H', data, 68, 0x8664)
        exe = self.game / 'PoseidonGame.exe'
        exe.write_bytes(data)
        with patch.object(core.subprocess, 'check_output', return_value='3.05\n'):
            VERIFY_GAME(self.game)
            exe.write_bytes(data + b'different storefront bytes')
            VERIFY_GAME(self.game)
        with patch.object(core.subprocess, 'check_output', return_value='3.06\n'):
            with self.assertRaisesRegex(ValueError, 'Unsupported Remastered version'):
                VERIFY_GAME(self.game)
        core.struct.pack_into('<H', data, 68, 0x14c)
        exe.write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'Windows x64'):
            VERIFY_GAME(self.game)

    def test_compatibility_ignores_unconsumed_assets_and_extra_missions(self):
        unrelated = self.game / 'Worlds/custom.wrp'
        unrelated.parent.mkdir()
        unrelated.write_bytes(b'player asset')
        manifest = dict(self.manifest, tables=[{'rows': [['STR', '中', '中', ['row', self.rel, 'STR']]]}],
                        edits=[], sources={**self.manifest['sources'], 'Worlds/custom.wrp': 'a' * 64})
        extra = self.game / 'Missions/player.eden/mission.sqm'
        extra.parent.mkdir(parents=True)
        extra.write_bytes(b'player mission')
        core.verify_sources(self.game, manifest)
        self.assertEqual(core.source_inputs(manifest), self.manifest['sources'])
        (self.game / self.rel).write_bytes(b'incompatible critical table')
        with self.assertRaisesRegex(ValueError, 'Restore this required file'):
            core.verify_sources(self.game, manifest)
        self.assertEqual(extra.read_bytes(), b'player mission')

    def test_standalone_mod_bank_preserves_members_and_campaigns_keep_backups(self):
        root = self.root / 'patch'
        self.fake_reconstruct(self.game, self.payload, root)
        rel = 'Resistance/player.noe'
        original = self.game / 'Missions' / rel
        original.mkdir(parents=True)
        (original / 'mission.sqm').write_bytes(b'original mission logic')
        (original / 'extra.txt').write_bytes(b'player addition')
        translated = root / 'standalone' / rel
        translated.mkdir(parents=True)
        (translated / 'stringtable.utf8.csv').write_bytes(b'Chinese table')
        outputs = CONTENT_OUTPUTS(root, self.game, self.root / core.MOD)
        self.assertIn(self.rel, outputs)
        self.assertFalse((self.root / core.MOD / 'Campaigns').exists())
        from build_labels import pbo_parts
        members = pbo_parts(outputs[core.MOD + '/Missions/' + rel + '.pbo'].read_bytes())[2]
        self.assertEqual(members, {b'mission.sqm': b'original mission logic',
                                  b'extra.txt': b'player addition', b'stringtable.utf8.csv': b'Chinese table'})
        self.assertEqual((self.game / self.rel).read_bytes(), self.original)

    def test_space_estimate_does_not_count_hardlinked_stock_assets(self):
        stock = self.game / 'AddOns/stock.pbo'
        stock.parent.mkdir()
        stock.write_bytes(b'stock asset is not copied')
        manifest = dict(self.manifest, sources={**self.manifest['sources'], 'AddOns/stock.pbo': 'unused'})
        small = core.required_space(self.game, self.payload, self.manifest)
        self.assertEqual(core.required_space(self.game, self.payload, manifest), small)
        generated = self.game / 'AddOns/Noe.pbo'
        with generated.open('wb') as stream:
            stream.truncate(1024**2)
        manifest['sources']['AddOns/Noe.pbo'] = 'unused'
        self.assertGreaterEqual(core.required_space(self.game, self.payload, manifest), small + 2 * 1024**2)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.game = self.root / 'game'
        self.game.mkdir()
        self.payload = self.root / 'payload'
        self.payload.mkdir()
        self.rel = 'Campaigns/1985/missions/test.eden/stringtable.utf8.csv'
        self.original = b'original stock bytes\r\n'
        p = self.game / self.rel
        p.parent.mkdir(parents=True)
        p.write_bytes(self.original)
        self.manifest = {'schema': 1, 'sources': {self.rel: core.digest(self.original)}, 'files': {}}
        (self.payload / 'payload.json').write_text(json.dumps(self.manifest))
        self.addCleanup(patch.stopall)
        patch.object(core, 'check_idle').start()
        patch.object(core, 'verify_game').start()
        patch.object(core, 'run_builders').start()
        patch.object(core, 'reconstruct', self.fake_reconstruct).start()
        # Keep the established replacement/restoration fault tests exercising
        # legacy loose-file receipts; current layout is checked separately.
        patch.object(core, 'content_outputs', side_effect=lambda root, game, mod:
                     {self.rel: root / 'campaign/1985/missions/test.eden/stringtable.utf8.csv'}).start()

    def fake_reconstruct(self, game, payload, out):
        for rel, data in [('campaign/1985/missions/test.eden/stringtable.utf8.csv', b'localized'),
                          ('mod/bin/stringtable.utf8.csv', b'Chinese data'),
                          ('font/cwr_body.ttf', b'font-SC'),
                          ('font/ChineseTraditional/cwr_body.ttf', b'font-TC'),
                          ('font/OFL.txt', b'font license'), ('font/NOTICE.md', b'SC attribution'),
                          ('font/ChineseTraditional/NOTICE.md', b'TC attribution')]:
            p = out / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        return self.manifest

    def install(self, **kwargs):
        return core.install(self.game, self.payload, **kwargs)

    def test_install_reinstall_uninstall_exact_and_unrelated(self):
        unrelated = self.game / 'user-save'
        unrelated.write_bytes(b'keep')
        for rel in ('@personal-mod/data', 'Users/player/save'):
            path = self.game / rel
            path.parent.mkdir(parents=True)
            path.write_bytes(b'untouched')
        receipt = self.install()
        (self.payload / 'payload.json').write_text(json.dumps(self.manifest, indent=4))
        self.assertEqual(self.install(), receipt)
        self.assertEqual((self.game / core.STATE / 'backup' / self.rel).read_bytes(), self.original)
        self.assertEqual(core.uninstall(self.game), [])
        self.assertEqual((self.game / self.rel).read_bytes(), self.original)
        self.assertEqual(unrelated.read_bytes(), b'keep')
        for rel in ('@personal-mod/data', 'Users/player/save'):
            self.assertEqual((self.game / rel).read_bytes(), b'untouched')
        self.assertFalse((self.game / core.MOD).exists())
        self.assertFalse((self.game / core.STATE).exists())
        self.assertEqual(self.install()['files'], receipt['files'])

    def test_modified_file_is_preserved_and_reinstall_rejected(self):
        self.install()
        (self.game / self.rel).write_bytes(b'user edit')
        with self.assertRaisesRegex(ValueError, 'User modified'):
            self.install()
        self.assertEqual(core.uninstall(self.game), [self.rel])
        self.assertEqual((self.game / self.rel).read_bytes(), b'user edit')
        self.assertEqual((self.game / core.STATE / 'backup' / self.rel).read_bytes(), self.original)
        (self.game / self.rel).write_bytes(self.original)
        self.assertEqual(core.uninstall(self.game), [])

    def test_injected_failure_rolls_back(self):
        with self.assertRaisesRegex(OSError, 'Injected'):
            self.install(fail_after=8)  # Includes replacement of the original loose table.
        self.assertEqual((self.game / self.rel).read_bytes(), self.original)
        self.assertEqual([p.relative_to(self.game).as_posix() for p in self.game.rglob('*') if p.is_file()], [self.rel])

    def test_interrupted_journal_recovers(self):
        with patch.object(core, 'recover', side_effect=RuntimeError('simulated process interruption')):
            with self.assertRaises(RuntimeError):
                self.install(fail_after=8)
        core.recover(self.game)
        self.assertEqual((self.game / self.rel).read_bytes(), self.original)
        self.assertFalse((self.game / core.STATE).exists())

    def test_sigint_at_commit_boundary_preserves_uninstall_metadata(self):
        unlink = Path.unlink
        state = self.game / core.STATE
        pending = state / 'pending.json'
        for committed in (False, True):
            with self.subTest(committed=committed):
                def interrupt_commit(path, *args, **kwargs):
                    if path == pending and not committed:
                        signal.raise_signal(signal.SIGINT)
                    result = unlink(path, *args, **kwargs)
                    if path == pending and committed:
                        signal.raise_signal(signal.SIGINT)
                    return result
                with patch.object(Path, 'unlink', interrupt_commit):
                    with self.assertRaises(KeyboardInterrupt):
                        self.install()
                if committed:
                    self.assertFalse(pending.exists())
                    receipt_path = state / 'receipt.json'
                    receipt_bytes = receipt_path.read_bytes()
                    receipt = json.loads(receipt_bytes)
                    self.assertEqual(receipt['status'], 'installed')
                    self.assertEqual((state / 'backup' / self.rel).read_bytes(), self.original)
                    for rel, item in receipt['files'].items():
                        self.assertEqual(core.digest((self.game / rel).read_bytes()), item['installed'])
                    self.assertEqual(self.install(), receipt)
                    self.assertEqual(receipt_path.read_bytes(), receipt_bytes)
                    self.assertEqual((state / 'backup' / self.rel).read_bytes(), self.original)
                    self.assertEqual(core.uninstall(self.game), [])
                self.assertEqual((self.game / self.rel).read_bytes(), self.original)
                self.assertFalse(state.exists())
                self.assertFalse((self.game / core.RETIRED).exists())
                self.assertEqual([p.relative_to(self.game).as_posix()
                                  for p in self.game.rglob('*') if p.is_file()], [self.rel])

    def leave_pending_install(self):
        with patch.object(core, 'recover', side_effect=RuntimeError('process stopped')):
            with self.assertRaises(RuntimeError):
                self.install(fail_after=8)

    def test_restore_retry_recognizes_both_complete_temporary_hashes(self):
        for operation in ('uninstall', 'recover'):
            for data in (b'localized', self.original):
                with self.subTest(operation=operation, data=data):
                    if operation == 'recover':
                        self.leave_pending_install()
                    else:
                        self.install()
                    tmp = self.game / (self.rel + '.crwc-tmp')
                    # Process died after staging a complete copy, before its rename.
                    tmp.write_bytes(data)
                    getattr(core, operation)(self.game)
                    self.assertFalse(tmp.exists())
                    self.assertEqual((self.game / self.rel).read_bytes(), self.original)
                    self.assertFalse((self.game / core.STATE).exists())

    def test_unknown_restore_temporary_is_preserved(self):
        self.install()
        tmp = self.game / (self.rel + '.crwc-tmp')
        tmp.write_bytes(b'user temp or incomplete copy')
        self.assertEqual(core.uninstall(self.game), [self.rel + '.crwc-tmp'])
        self.assertEqual(tmp.read_bytes(), b'user temp or incomplete copy')
        self.assertEqual((self.game / core.STATE / 'backup' / self.rel).read_bytes(), self.original)

    def test_preparation_failure_never_publishes_incomplete_state(self):
        copy = core.shutil.copyfile
        journal = core.atomic_json
        def stop_copy(source, dest, *args, **kwargs):
            result = copy(source, dest, *args, **kwargs)
            if 'backup' in Path(dest).parts:
                self.assertFalse((self.game / core.STATE).exists())
                raise OSError('interrupted backup preparation')
            return result
        def stop_journal(path, value):
            if path.parent.name == 'state':
                self.assertFalse((self.game / core.STATE).exists())
                raise OSError('interrupted journal preparation')
            return journal(path, value)
        for attribute, fault in [('copyfile', stop_copy), ('atomic_json', stop_journal)]:
            with self.subTest(stage=attribute):
                owner = core.shutil if attribute == 'copyfile' else core
                with patch.object(owner, attribute, fault):
                    with self.assertRaisesRegex(OSError, 'interrupted'):
                        self.install()
                self.assertFalse((self.game / core.STATE).exists())
                self.assertEqual((self.game / self.rel).read_bytes(), self.original)
                self.install()
                core.uninstall(self.game)

    def test_publication_interruption_recovers_complete_state(self):
        rename = core.os.rename
        def stop_after_publish(source, dest):
            result = rename(source, dest)
            if dest == self.game / core.STATE:
                raise OSError('interrupted after atomic publication')
            return result
        with patch.object(core.os, 'rename', stop_after_publish):
            with self.assertRaisesRegex(OSError, 'publication'):
                self.install()
        state = self.game / core.STATE
        self.assertTrue((state / 'pending.json').is_file())
        self.assertEqual((state / 'backup' / self.rel).read_bytes(), self.original)
        core.recover(self.game)
        self.assertEqual((self.game / self.rel).read_bytes(), self.original)
        self.assertFalse(state.exists())

    def test_retired_cleanup_resumes_from_all_entry_points(self):
        unlink = Path.unlink
        for pending in (False, True):
            for entry in ('install', 'uninstall', 'recover'):
                with self.subTest(pending=pending, entry=entry):
                    if pending:
                        self.leave_pending_install()
                    else:
                        self.install()
                    backup = self.game / core.RETIRED / 'backup' / self.rel
                    def stop_cleanup(path, *args, **kwargs):
                        result = unlink(path, *args, **kwargs)
                        if path == backup:
                            raise OSError('interrupted backup retirement')
                        return result
                    with patch.object(Path, 'unlink', stop_cleanup):
                        with self.assertRaisesRegex(OSError, 'retirement'):
                            getattr(core, 'recover' if pending else 'uninstall')(self.game)
                    self.assertEqual((self.game / self.rel).read_bytes(), self.original)
                    self.assertFalse((self.game / core.STATE).exists())
                    self.assertTrue((self.game / core.RETIRED).is_dir())
                    if entry == 'install':
                        self.install()
                        core.uninstall(self.game)
                    else:
                        getattr(core, entry)(self.game)
                    self.assertFalse((self.game / core.RETIRED).exists())
                    self.assertFalse((self.game / core.STATE).exists())

    def test_retirement_rename_and_final_journal_deletion_are_resumable(self):
        rename, unlink = core.os.rename, Path.unlink
        for point in ('rename', 'journal'):
            with self.subTest(point=point):
                self.install()
                def stop_rename(source, dest):
                    result = rename(source, dest)
                    if dest == self.game / core.RETIRED:
                        raise OSError('interrupted retirement rename')
                    return result
                def stop_unlink(path, *args, **kwargs):
                    result = unlink(path, *args, **kwargs)
                    if path == self.game / core.RETIRED / 'receipt.json':
                        raise OSError('interrupted final journal deletion')
                    return result
                owner, name, fault = ((core.os, 'rename', stop_rename) if point == 'rename'
                                      else (Path, 'unlink', stop_unlink))
                with patch.object(owner, name, fault):
                    with self.assertRaisesRegex(OSError, 'interrupted'):
                        core.uninstall(self.game)
                core.recover(self.game)
                self.assertFalse((self.game / core.RETIRED).exists())
                self.assertEqual((self.game / self.rel).read_bytes(), self.original)

    def test_unknown_retired_state_is_preserved(self):
        self.install()
        with patch.object(core, 'resume_retired', side_effect=OSError('stopped cleanup')):
            # Retire only after restoring, not at uninstall's initial resume check.
            record = json.loads((self.game / core.STATE / 'receipt.json').read_text())
            self.assertEqual(core.restore(self.game, record), [])
            with self.assertRaises(OSError):
                core.clear_state(self.game, record)
        extra = self.game / core.RETIRED / 'notes.txt'
        extra.write_bytes(b'user notes')
        for operation in (self.install, lambda: core.recover(self.game), lambda: core.uninstall(self.game)):
            with self.assertRaisesRegex(ValueError, 'Preserved unrecognized'):
                operation()
        self.assertEqual(extra.read_bytes(), b'user notes')
        self.assertEqual((self.game / core.RETIRED / 'backup' / self.rel).read_bytes(), self.original)
        extra.unlink()
        core.recover(self.game)

    def test_corrupt_backup_blocks_all_restoration(self):
        self.install()
        (self.game / core.STATE / 'backup' / self.rel).write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'Corrupt backup'):
            core.uninstall(self.game)
        self.assertEqual((self.game / self.rel).read_bytes(), b'localized')
        self.assertTrue((self.game / core.MOD).exists())

    def test_unknown_state_file_is_not_deleted(self):
        self.install()
        extra = self.game / core.STATE / 'notes.txt'
        extra.write_bytes(b'user notes')
        with self.assertRaisesRegex(ValueError, 'Preserved unrecognized'):
            core.uninstall(self.game)
        self.assertEqual(extra.read_bytes(), b'user notes')
        extra.unlink()
        self.assertEqual(core.uninstall(self.game), [])

    def test_bad_source_conflict_and_space_preflight(self):
        (self.game / self.rel).write_bytes(b'unsupported')
        with self.assertRaisesRegex(ValueError, 'Incompatible Remastered 3.05 source'):
            self.install()
        (self.game / self.rel).write_bytes(self.original)
        conflict = self.game / core.MOD
        conflict.mkdir()
        with self.assertRaisesRegex(ValueError, 'Conflicting existing'):
            self.install()
        conflict.rmdir()
        with patch.object(core.shutil, 'disk_usage', return_value=type('Usage', (), {'free': 0})()):
            with self.assertRaisesRegex(ValueError, 'Insufficient'):
                self.install()
        self.assertFalse((self.game / core.STATE).exists())

    def test_preexisting_temporary_file_not_overwritten(self):
        tmp = self.game / (self.rel + '.crwc-tmp')
        tmp.write_bytes(b'user temp')
        with self.assertRaisesRegex(ValueError, 'Conflicting temporary|Unrecognized stock input'):
            self.install()
        self.assertEqual(tmp.read_bytes(), b'user temp')
        self.assertFalse((self.game / core.STATE).exists())

    def test_unrelated_extra_content_is_allowed_untouched(self):
        extra = self.game / 'Campaigns/1985/config.cpp'
        extra.write_bytes(b'unsupported loose override')
        self.install()
        self.assertEqual(core.uninstall(self.game), [])
        self.assertEqual(extra.read_bytes(), b'unsupported loose override')
        self.assertEqual((self.game / self.rel).read_bytes(), self.original)

    def test_paths_and_receipt_are_bounded(self):
        for rel in ('../outside', 'C:/outside', 'folder/file:stream', 'folder\\file', 'folder/file.', 'folder/CON.txt'):
            with self.assertRaises(ValueError):
                core.target(self.game, rel)
        with self.assertRaisesRegex(ValueError, 'Unexpected receipt'):
            core.validate_record(self.game, {'schema': 1, 'files': {'user-save': {'original': None, 'installed': 'a'*64}}})

    def test_actual_stock_csv_reader_quoted_comma(self):
        path = 'stock.utf8.csv'
        rows = [core.HEADER[:9], ['STR_TEST', 'English', 'French, with comma', 'Spanish', 'Italian',
                                'Czech', 'Polish', 'German', 'Russian']]
        (self.game / path).write_bytes(core.csv_bytes(rows))
        self.assertEqual(core.read_stock(self.game, path)['STR_TEST'], rows[1])

    def test_failed_journal_commit_preserves_prior_journal(self):
        path = self.root / 'pending.json'
        path.write_bytes(b'old journal')
        with patch.object(core.os, 'replace', side_effect=OSError('failed atomic replacement')):
            with self.assertRaises(OSError):
                core.atomic_json(path, {'new': 'journal'})
        self.assertEqual(path.read_bytes(), b'old journal')
        self.assertFalse(path.with_suffix('.tmp').exists())
        path.with_suffix('.tmp').write_bytes(b'user conflict')
        with self.assertRaises(FileExistsError):
            core.atomic_json(path, {'new': 'journal'})
        self.assertEqual(path.with_suffix('.tmp').read_bytes(), b'user conflict')

    def test_reconstruction_preserves_order_stock_columns_and_comments(self):
        source = 'MPMissions/test.eden/stringtable.utf8.csv'
        stock = [core.HEADER[:9] + ['COMMENT'],
                 ['STR_MixedCase', 'English %s', 'French, comma %s', 'ES %s', 'IT %s',
                  'CZ %s', 'PL %s', 'DE %s', 'RU %s', 'original comment'],
                 ['STR_second', 'Second', '', '', '', '', '', '', '', 'another comment']]
        path = self.game / source
        path.parent.mkdir(parents=True)
        path.write_bytes(core.csv_bytes(stock))
        expected = [core.HEADER + ['COMMENT'],
                    stock[1][:9] + ['中文 %s', '中文 %s'] + stock[1][9:],
                    stock[2][:9] + ['第二', '第二'] + stock[2][9:]]
        manifest = {'schema': 1, 'tables': [{'path': 'multiplayer/' + source, 'header': expected[0],
                    'sha256': core.digest(core.csv_bytes(expected)),
                    'rows': [[r[0], r[9], r[10], ['row', source, r[0]]] for r in expected[1:]]}],
                    'edits': [], 'files': {}}
        (self.payload / 'payload.json').write_text(json.dumps(manifest))
        out = self.root / 'reconstructed'
        with patch.object(core, 'stock_globals', return_value={}):
            RECONSTRUCT(self.game, self.payload, out)
        self.assertEqual((out / 'multiplayer' / source).read_bytes(), core.csv_bytes(expected))
        manifest['tables'][0]['sha256'] = '0' * 64
        (self.payload / 'payload.json').write_text(json.dumps(manifest))
        with patch.object(core, 'stock_globals', return_value={}):
            with self.assertRaisesRegex(ValueError, 'Reconstruction differs'):
                RECONSTRUCT(self.game, self.payload, self.root / 'bad-output')


if __name__ == '__main__':
    unittest.main()
