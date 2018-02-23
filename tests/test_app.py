import unittest

from meta.app_creator import _to_date


class TestToDate(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(_to_date(''), '')

    def test_valid_case(self):
        self.assertEqual(_to_date(20171231), '31.12.2017')
