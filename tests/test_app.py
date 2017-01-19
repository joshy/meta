import unittest
from meta.app import app, CONNECTION

class TestApp(unittest.TestCase):
    def test_cmd(self):
        expected = '-aet AE_TITLE -aec AE_CALLED 127.0.0.1 104 +P 11110 /Applications/dcmtk/dcm.in'
        self.assertEqual(expected, CONNECTION)
