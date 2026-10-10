"""Focused release exclusions; all fixtures are synthetic and temporary."""
import tempfile
import unittest
import zipfile
import subprocess
from pathlib import Path

from build_release import package_zip, require_clean_tracked


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cwrc-package-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.files = self.root / 'files'
        self.client = self.files / '@cwr-chinese/client/PoseidonGame.exe'
        self.client.parent.mkdir(parents=True)
        self.client.write_bytes(b'modified-client-stand-in')
        self.stock = self.root / 'stock.exe'
        self.stock.write_bytes(b'stock-executable-stand-in')
        self.output = self.root / 'cwr-chinese.zip'

    def package(self):
        package_zip(self.files, self.output, self.stock)

    def test_packaging_requires_clean_tracked_sources(self):
        repo = self.root / 'repo'
        repo.mkdir()
        def git(*args):
            subprocess.run(['git', '-c', 'user.name=Packaging test', '-c',
                            'user.email=test@example.invalid', *args], cwd=repo,
                           check=True, capture_output=True)
        git('init')
        tracked = repo / 'source.txt'
        tracked.write_text('committed')
        git('add', '.')
        git('commit', '-m', 'fixture')
        (repo / 'untracked-build-output').write_text('ignored for cleanliness')
        require_clean_tracked(repo, 'localization')
        tracked.write_text('modified')
        for label in ('localization', 'client'):
            with self.assertRaisesRegex(ValueError, f'Commit the {label}'):
                require_clean_tracked(repo, label)
        git('add', 'source.txt')
        with self.assertRaisesRegex(ValueError, 'Commit the localization'):
            require_clean_tracked(repo, 'localization')

    def test_stock_executable_is_rejected_before_archive_creation(self):
        for executable in (self.client, self.files / 'cwr-chinese.exe'):
            with self.subTest(executable=executable):
                executable.write_bytes(self.stock.read_bytes())
                with self.assertRaisesRegex(ValueError, 'Original game executable leaked'):
                    self.package()
                self.assertFalse(self.output.exists())
                executable.write_bytes(b'modified-executable')

    def test_modified_client_openal_and_apl_sa_content_are_allowed(self):
        for relative in ('@cwr-chinese/client/OpenAL32.dll', '@cwr-chinese/AddOns/Noe.pbo',
                         '@cwr-chinese/bin/config.bin', '@cwr-chinese/localization/Campaigns/1985/description.ext'):
            file = self.files / relative
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(b'allowed-content-stand-in')
        self.package()
        with zipfile.ZipFile(self.output) as archive:
            self.assertEqual(len(archive.namelist()), 5)
            self.assertTrue(all(name.startswith('Remastered/') for name in archive.namelist()))
            self.assertEqual(archive.read('Remastered/@cwr-chinese/client/PoseidonGame.exe'), self.client.read_bytes())

    def test_launcher_is_allowed_without_bundled_runtime(self):
        (self.files / 'cwr-chinese.exe').write_bytes(b'new-native-launcher')
        self.package()
        with zipfile.ZipFile(self.output) as archive:
            self.assertEqual(set(archive.namelist()), {
                'Remastered/@cwr-chinese/client/PoseidonGame.exe',
                'Remastered/cwr-chinese.exe',
            })
            self.assertEqual(archive.read('Remastered/cwr-chinese.exe'), b'new-native-launcher')


if __name__ == '__main__':
    unittest.main()
