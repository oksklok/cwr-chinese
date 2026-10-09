"""Focused release exclusions; all fixtures are synthetic and temporary."""
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_release import package_zip


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cwrc-package-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.files = self.root / 'files'
        self.client = self.files / '@CWRC/client/PoseidonGame.exe'
        self.client.parent.mkdir(parents=True)
        self.client.write_bytes(b'modified-client-stand-in')
        self.stock = self.root / 'stock.exe'
        self.stock.write_bytes(b'stock-executable-stand-in')
        self.output = self.root / 'CWRC.zip'

    def package(self):
        package_zip(self.files, self.output, self.stock)

    def test_stock_executable_is_rejected_before_archive_creation(self):
        self.client.write_bytes(self.stock.read_bytes())
        with self.assertRaisesRegex(ValueError, 'Original game executable leaked'):
            self.package()
        self.assertFalse(self.output.exists())

    def test_microsoft_runtimes_are_rejected_anywhere_in_staging(self):
        for relative in ('@CWRC/client/vcruntime140.dll',
                         '@CWRC/source/local-build/VCRUNTIME140_1.DLL',
                         '@CWRC/client/msvcp140.dll'):
            with self.subTest(relative=relative):
                stale = self.files / relative
                stale.parent.mkdir(parents=True, exist_ok=True)
                stale.write_bytes(b'stale-runtime-stand-in')
                with self.assertRaisesRegex(ValueError, 'Microsoft runtime must not be bundled'):
                    self.package()
                self.assertFalse(self.output.exists())
                stale.unlink()

    def test_modified_client_openal_and_apl_sa_content_are_allowed(self):
        for relative in ('@CWRC/client/OpenAL32.dll', '@CWRC/AddOns/Noe.pbo',
                         '@CWRC/bin/config.bin', '@CWRC/localization/Campaigns/1985/description.ext'):
            file = self.files / relative
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(b'allowed-content-stand-in')
        self.package()
        with zipfile.ZipFile(self.output) as archive:
            self.assertEqual(len(archive.namelist()), 5)
            self.assertEqual(archive.read('@CWRC/client/PoseidonGame.exe'), self.client.read_bytes())


if __name__ == '__main__':
    unittest.main()
