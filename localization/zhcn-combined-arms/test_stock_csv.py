"""Regression for stock CSV spaces before quoted commas; run with unittest."""
import csv
import io
import tempfile
import unittest
from pathlib import Path

from validate_resistance import stock_csv_rows
from validate_ui import read_rows


class StockCsvTests(unittest.TestCase):
    def test_space_before_quoted_comma_preserves_columns(self):
        text = ('STR_CRATE, "Ammo Crates (West, AddOns)", '
                '"Caisses de munitions (Ouest, AddOns)", '
                '"Casse di munizioni (Occidente, AddOns)"\r\n')
        expected = [['STR_CRATE', 'Ammo Crates (West, AddOns)',
                     'Caisses de munitions (Ouest, AddOns)',
                     'Casse di munizioni (Occidente, AddOns)']]
        self.assertNotEqual(list(csv.reader(io.StringIO(text))), expected)
        self.assertEqual(stock_csv_rows(text, strict=True), expected)
        with tempfile.TemporaryDirectory(prefix='cwrc-stock-csv-') as directory:
            source = Path(directory) / 'stringtable.csv'
            source.write_bytes(text.encode('ascii'))
            for legacy in (False, True):
                self.assertEqual(read_rows(source, legacy=legacy)['STR_CRATE'], expected[0])

    def test_quoted_spaces_escaped_quotes_and_physical_breaks_survive(self):
        text = 'STR_TEST, " leading, ""quoted""\nsecond line ", trailing \r\n'
        self.assertEqual(stock_csv_rows(text, strict=True),
                         [['STR_TEST', ' leading, "quoted"\nsecond line ', 'trailing ']])

    def test_empty_columns_do_not_shift(self):
        self.assertEqual(stock_csv_rows('STR_TEST, , "English, text", ,\n', strict=True),
                         [['STR_TEST', '', 'English, text', '', '']])


if __name__ == '__main__':
    unittest.main()
