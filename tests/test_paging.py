import unittest
from meta.paging import calc


class TestQueryStuff(unittest.TestCase):
    def test_update_url1(self):
        r = calc(200, 'http://localhost', '1')
        self.assertEqual(0, len(r))

    def test_update_url2(self):
        r = calc(1200, 'http://localhost', '1')
        self.assertEqual('http://localhost?offset=500', r[1][1])
        self.assertEqual(3, len(r))
