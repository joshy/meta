import unittest
from meta.paging import calc


class TestQueryStuff(unittest.TestCase):
    def test_update_url(self):
        r = calc(200, 'http://localhost', '1')
        self.assertEqual(0, len(r))

    def test_update_url(self):
        r = calc(700, 'http://localhost', '1')
        self.assertEqual(1, len(r))
