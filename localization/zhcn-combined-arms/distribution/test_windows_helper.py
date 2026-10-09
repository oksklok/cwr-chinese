import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import windows_helper as helper


class WrapperEntryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        self.state = self.game / helper.core.STATE
        self.state.mkdir()

    def run_helper(self, operation):
        with patch.object(sys, 'argv', ['cwrc-helper', operation, str(self.game)]):
            return helper.main()

    def test_interrupted_install_recovers_before_reinstall(self):
        (self.state / 'pending.json').write_text('{}')
        calls = []
        with patch.object(helper.core, 'recover', side_effect=lambda _: calls.append('recover')), \
             patch.object(helper.core, 'install', side_effect=lambda *a: calls.append('install')):
            self.assertEqual(self.run_helper('install'), 0)
        self.assertEqual(calls, ['recover', 'install'])

    def test_restore_conflict_is_nonzero_for_the_uninstaller_gate(self):
        with patch.object(helper.core, 'uninstall', return_value=['modified.csv']):
            self.assertEqual(self.run_helper('uninstall'), 2)
        self.assertTrue(self.state.exists())

    def test_recovery_error_prevents_install(self):
        (self.state / 'pending.json').write_text('{}')
        with patch.object(helper.core, 'recover', side_effect=ValueError('modified backup')), \
             patch.object(helper.core, 'install') as install:
            self.assertEqual(self.run_helper('install'), 1)
            install.assert_not_called()
        self.assertTrue((self.state / 'pending.json').exists())


if __name__ == '__main__':
    unittest.main()
