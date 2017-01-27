import unittest
from meta.command import base_command, transfer_command
from meta.app import app

class TestCommand(unittest.TestCase):

    def test_base_command(self):
        expected = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/movescu -v -S -k QueryRetrieveLevel=SERIES -aet AE_TITLE -aec AE_CALLED 127.0.0.1 104 +P 11110'
        self.assertEqual(expected, base_command())

    def test_tranfer(self):
        expected = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/movescu -v -S -aem SRSYVMS01 -aet AE_TITLE -aec GE 10.247.12.5 4100 +P 4101 -k StudyInstanceUID=12345 /Applications/dcmtk/dcm.in'
        self.assertMultiLineEqual(expected, transfer_command('syngo', '12345'))