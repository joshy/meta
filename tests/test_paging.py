import unittest
from meta.paging import calc


class TestQueryStuff(unittest.TestCase):
    def test_update_url1(self):
        result = calc(200, 'http://localhost', '1', 100)
        self.assertEqual(2, len(result))

    def test_update_url2(self):
        result = calc(1200, 'http://localhost', '1', 100)
        self.assertEqual('http://localhost?offset=100', result[1][1])
        self.assertEqual(12, len(result))
