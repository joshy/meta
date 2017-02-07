import unittest
from meta.command import base_command, transfer_command
from meta.app import DCMTK_CONFIG, PACS_CONFIG

class TestCommand(unittest.TestCase):

    def test_base_command(self):
        expected = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/movescu -v -S -k QueryRetrieveLevel=SERIES -aet AE_TITLE -aec AE_CALLED 127.0.0.1 104 +P 11110'
        self.assertEqual(expected, base_command(DCMTK_CONFIG, PACS_CONFIG))

    def test_tranfer(self):
        expected = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/movescu -v -S -aem SRSYVMS01 -aet AE_TITLE -aec AE_CALLED 127.0.0.1 104 +P 11110 -k StudyInstanceUID=12345 /Applications/dcmtk/dcm.in'
        self.assertEqual(expected, transfer_command(DCMTK_CONFIG, PACS_CONFIG, 'syngo', '12345'))