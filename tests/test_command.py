import unittest
from meta.command import base_command, transfer_command
from meta.app import app

class TestCommand(unittest.TestCase):
    app.config.from_pyfile('test_config.cfg', silent=True)
    def test_base_command(self):
        expected = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/movescu -v -S -k QueryRetrieveLevel=SERIES -aet YETI -aec AE_CALLED 127.0.0.1 104 +P 11110 /Applications/dcmtk/dcm.in'
        self.assertEqual(expected, base_command())

    def test_tranfer(self):
        expected = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/movescu -v -S -aem SRSYVMS01 -aet MC526512B -aec GE 10.247.12.5 4100 +P 4101 /Applications/dcmtk/dcm.in'
        self.assertMultiLineEqual(expected, transfer_command('syngo'))