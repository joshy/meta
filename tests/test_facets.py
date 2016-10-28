import unittest
from meta.facets import prepare_facets


class TestFacetsStuff(unittest.TestCase):
    def test_update_url(self):
        facets = {'count': 94,
                  'SeriesDescription':
                  {'buckets':
                   [{'count': 94, 'val': 't2_haste_fs_thick_slab'}]},
                  'StudyDescription':
                  {'buckets': [{'count': 92, 'val': 'MRI Abdomen'},
                               {'count': 2, 'val': 'MRI Becken'}]}
                  }

        url = 'http://localhost:5000/search?query=%2A&SeriesDescription=%22t2_haste_fs_thick_slab%22'
        r = prepare_facets(facets, url)
        series_buckets = r.get('SeriesDescription').get('buckets')
        study_buckets = r.get('StudyDescription').get('buckets')
        self.assertEqual(1, len(series_buckets))
        self.assertEqual(2, len(study_buckets))
