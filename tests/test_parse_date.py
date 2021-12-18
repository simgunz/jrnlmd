import unittest

from jrnlmd.jrnlmd import parse_date


class TestDateParser(unittest.TestCase):
    def test_date_parser(self):
        txt_date = "12nov2021"
        iso_date = parse_date(txt_date)
        self.assertEqual("2021-11-12", iso_date)

    def test_date_parser_unparsable(self):
        txt_date = "aaaa"
        iso_date = parse_date(txt_date)
        self.assertEqual(None, iso_date)

    def test_date_parser_single_char(self):
        txt_date = "a"
        iso_date = parse_date(txt_date)
        self.assertEqual(None, iso_date)
