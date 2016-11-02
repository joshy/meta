import unittest
from meta.grouping import group


class TestGroupingStuff(unittest.TestCase):
    def test_grouping(self):
        r = group(test_date)
        # same group size as before
        groups = r['groups']
        self.assertEqual(2, len(groups))
        # has grouped docs
        self.assertTrue('by_AccessionNumber' in groups[0])
        self.assertTrue('by_AccessionNumber' in groups[1])


test_date = {'groups': [
    {'groupValue': 'ABC',
     'doclist': {'numFound': 3, 'start': 0,
                 'docs': [
                     {
                         'AccessionNumber': '1',
                         'StudyID': '1',
                     },
                     {
                         'AccessionNumber': '2',
                         'StudyID': '2',
                     },
                     {
                         'AccessionNumber': '2',
                         'StudyID': '2'
                     }
                 ]}
     },
    {
        'groupValue': 'DEF',
        'doclist': {'numFound': 3, 'start': 0,
                    'docs': [
                        {
                            'AccessionNumber': '3',
                            'StudyID': '20725498'},
                        {
                            'AccessionNumber': '3',
                            'StudyID': '20725498'},
                        {
                            'AccessionNumber': '3',
                            'StudyID': '20725498',
                        }
                    ]}
    }
]
}
