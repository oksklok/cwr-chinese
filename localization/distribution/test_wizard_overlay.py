"""Chinese briefing variants must not replace stock template HTML or logic."""
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from build_content import PATCH

sys.path.insert(0, str(PATCH / 'multiplayer'))
from build_missions import pack
from build_labels import pbo_parts


class WizardOverlayTests(unittest.TestCase):
    def test_chinese_html_is_added_without_changing_stock_members(self):
        spec = importlib.util.spec_from_file_location('wizard_builder', PATCH / 'wizard/build_templates.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory(prefix='cwrc-wizard-test-') as work:
            root = Path(work)
            game, source, mod = root / 'game', root / 'source', root / 'mod'
            relative = 'Templates/Test.Eden.pbo'
            stock = {'briefing.utf8.html': b'<p>$STR_ONE <a href="marker:start">$STR_TWO</a></p>',
                     'mission.sqm': b'unchanged mission logic', 'script.sqs': b'unchanged script',
                     'stringtable.utf8.csv': b'stock table'}
            data = pack(stock)
            (game / relative).parent.mkdir(parents=True)
            (game / relative).write_bytes(data)
            folder = source / relative.removesuffix('.pbo')
            folder.mkdir(parents=True)
            (source / 'stock-hashes.json').write_text(json.dumps({relative: hashlib.sha256(data).hexdigest()}))
            (folder / 'stringtable.utf8.csv').write_bytes(b'localized table')
            translated = stock['briefing.utf8.html'].replace(b' <a', b'<a')
            for language in ('ChineseSimplified', 'ChineseTraditional'):
                (folder / f'briefing.{language}.utf8.html').write_bytes(translated)
            with patch.object(builder, 'ROOT', source), patch.object(sys, 'argv', ['builder', str(game), '--mod-dir', str(mod)]):
                builder.main()
                with patch.object(sys, 'argv', sys.argv + ['--check']):
                    builder.main()
            members = pbo_parts((mod / relative).read_bytes())[2]
            self.assertEqual(len(members), len(stock) + 2)
            for name, value in stock.items():
                self.assertEqual(members[name.encode()], b'localized table' if name == 'stringtable.utf8.csv' else value)
            for language in ('ChineseSimplified', 'ChineseTraditional'):
                self.assertEqual(members[f'briefing.{language}.utf8.html'.encode()], translated)
            self.assertEqual((game / relative).read_bytes(), data)


if __name__ == '__main__':
    unittest.main()
