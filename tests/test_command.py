import unittest
from meta.command_creator import _get_base_command, construct_transfer_command
from meta.config import dcmtk_config, pacs_config

DCMTK_CONFIG = dcmtk_config({'DCMTK_BIN':'/usr/local/bin/',
                             'DCMIN': '/opt/dcm.in'})

PACS_CONFIG = pacs_config({'AE_TITLE':'AE_TITLE', 'AE_CALLED': 'AE_CALLED',
                           'PEER_ADDRESS': '127.0.0.1', 'PEER_PORT': 104,
                           'INCOMING_PORT': 11110})


class TestCommand(unittest.TestCase):
    def test_base_command(self):
        expected = '/usr/local/bin/movescu -v -S -k QueryRetrieveLevel=SERIES -aet AE_TITLE -aec AE_CALLED 127.0.0.1 104 +P 11110'
        self.assertEqual(expected, _get_base_command(DCMTK_CONFIG, PACS_CONFIG))

    def test_transfer(self):
        expected = '/usr/local/bin/movescu -v -S -aem SRSYVMS01 -aet AE_TITLE -aec AE_CALLED 127.0.0.1 104 +P 11110 -k StudyInstanceUID=12345 /opt/dcm.in'
        self.assertEqual(expected, construct_transfer_command(DCMTK_CONFIG, PACS_CONFIG, 'syngo', '12345'))
