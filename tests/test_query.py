import unittest
import meta.query

class TestQueryStuff(unittest.TestCase):

    def test_upper(self):
        args = {'q': 'foo', 'StartDate': '1.1.2016', 'EndDate': '31.12.2016',
                'StudyDescription': 'lorem'}
        result, raw = meta.query.json_body(args)
        print(raw)
        self.assertEqual(raw['query'], 'foo AND ')


if __name__ == '__main__':
    unittest.main()
