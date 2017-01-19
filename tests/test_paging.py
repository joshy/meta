import unittest
from meta.paging import calc


class TestQueryStuff(unittest.TestCase):
    def test_update_url1(self):
        result = calc(200, '1', 100)
        self.assertEqual(2, len(result))
        self.assertEqual(True, result[0][1])

    def test_update_url2(self):
        result = calc(1200, '1', 100)
        self.assertEqual(False, result[1][1])
        self.assertEqual(12, len(result))

    def test_active(self):
        result = calc(1200, '5', 100)
        self.assertEqual(True, result[4][1])
