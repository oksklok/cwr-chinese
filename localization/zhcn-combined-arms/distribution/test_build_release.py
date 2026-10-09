"""Focused release exclusions; all fixtures are synthetic and temporary."""
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_release import MSVC_RUNTIME, package_zip


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
        self.redist = self.root / 'redist'
        self.redist.mkdir()
        for name in MSVC_RUNTIME:
            (self.redist / name).write_bytes(b'current-redist-' + name.encode())

    def package(self):
        package_zip(self.files, self.output, self.stock, self.redist)

    def test_stock_executable_is_rejected_before_archive_creation(self):
        for executable in (self.client, self.files / 'cwr-chinese.exe'):
            with self.subTest(executable=executable):
                executable.write_bytes(self.stock.read_bytes())
                with self.assertRaisesRegex(ValueError, 'Original game executable leaked'):
                    self.package()
                self.assertFalse(self.output.exists())
                executable.write_bytes(b'modified-executable')

    def test_stale_or_unapproved_microsoft_runtimes_are_rejected(self):
        for relative in ('@cwr-chinese/client/vcruntime140.dll',
                         '@cwr-chinese/source/local-build/VCRUNTIME140_1.DLL',
                         '@cwr-chinese/client/msvcp140.dll',
                         '@cwr-chinese/client/msvcp140_2.dll'):
            with self.subTest(relative=relative):
                stale = self.files / relative
                stale.parent.mkdir(parents=True, exist_ok=True)
                stale.write_bytes(b'stale-runtime-stand-in')
                with self.assertRaisesRegex(ValueError, 'Unexpected or stale Microsoft runtime'):
                    self.package()
                self.assertFalse(self.output.exists())
                stale.unlink()

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

    def test_selected_app_local_runtime_and_launcher_are_allowed(self):
        (self.files / 'cwr-chinese.exe').write_bytes(b'new-native-launcher')
        for name in MSVC_RUNTIME:
            (self.client.parent / name).write_bytes((self.redist / name).read_bytes())
        self.package()
        with zipfile.ZipFile(self.output) as archive:
            self.assertEqual(len(archive.namelist()), 5)

            self.assertEqual(archive.read('Remastered/cwr-chinese.exe'), b'new-native-launcher')


if __name__ == '__main__':
    unittest.main()
