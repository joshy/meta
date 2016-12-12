import unittest
from meta.paging import calc


class TestQueryStuff(unittest.TestCase):
    def test_update_url1(self):
        r = calc(200, 'http://localhost', '1')
        self.assertEqual(2, len(r))

    def test_update_url2(self):
        r = calc(1200, 'http://localhost', '1')
        self.assertEqual('http://localhost?offset=100', r[1][1])
        self.assertEqual(12, len(r))
