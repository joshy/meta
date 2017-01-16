import unittest
from meta.command import base_command, transfer_command


class TestCommand(unittest.TestCase):

    def test_base_command(self):
        expected = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/movescu -v -S -k QueryRetrieveLevel=SERIES -aet SNOWFOX -aec AE_ARCH2_4PR 10.5.66.74 104 +P 11110 /Applications/dcmtk/dcm.in'
        self.assertEqual(expected, base_command())

    def test_tranfer(self):
        expected = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/movescu -v -S -aem SRSYVMS01 -aet MC526512B -aec GE 10.247.12.5 4100 +P 4101 /Applications/dcmtk/dcm.in'
        self.assertMultiLineEqual(expected, transfer_command('syngo'))