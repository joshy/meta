import unittest
from meta.app import CONNECTION


class TestApp(unittest.TestCase):

    def test_cmd(self):
        expected = '-aet SNOWFOX -aec AE_ARCH2_4PR 10.5.66.74 104 +P 11110 /Applications/dcmtk/dcm.in'
        self.assertEqual(expected, CONNECTION)
