import unittest

from tasks.download import DownloadTask
from tasks.command import create_download_command, create_transfer_command
from tasks.move import MoveTask
from meta.config import dcmtk_config, pacs_config
from unittest.mock import patch

DCMTK_CONFIG = dcmtk_config({'DCMTK_BIN':'/usr/local/bin/',
                             'DCMIN': '/opt/dcm.in'})

PACS_CONFIG = pacs_config({'AE_TITLE':'AE_TITLE', 'AE_CALLED': 'AE_CALLED',
                           'PEER_ADDRESS': '127.0.0.1', 'PEER_PORT': 104,
                           'INCOMING_PORT': 11110})


class TestCommand(unittest.TestCase):

    def test_get_command(self):
        with patch('tasks.command.makedirs') as mock_makedirs:
            mock_makedirs.return_value = None

            dt = DownloadTask(aet='aet',
                              aec='aec',
                              dcmin='/dcm.in',
                              movescu='/movescu',
                              peer_address='127.0.0.1',
                              peer_port='90',
                              incoming_port='102',
                              study_instance_uid = 'study_instance_uid',
                              series_instance_uid  = 'series_instance_uid',
                              patient_id = 'f',
                              accession_number='asdf',
                              series_number='1232',
                              dir_name='adsf')

            expected = ('/movescu -v -S -k QueryRetrieveLevel=SERIES -aet aet -aec aec 127.0.0.1 90 +P 102 --output-directory /data/image_data/adsf/f/asdf/1232 -k StudyInstanceUID=study_instance_uid -k SeriesInstanceUID=series_instance_uid /dcm.in')
            self.assertEqual(expected, create_download_command(dt))

    def test_transfer(self):
        mt = MoveTask(aet='aet',
                      aec='aec',
                      dcmin='/dcm.in',
                      movescu='/movescu',
                      peer_address='127.0.0.1',
                      peer_port='90',
                      incoming_port='102',
                      series_instance_uid ='12345',
                      target='teamplay')
        expected = (
            '/movescu '
            '-v -S -aem TEAMPLAY '
            '-aet aet '
            '-aec aec '
            '127.0.0.1 90 +P 102 '
            '-k StudyInstanceUID=12345 '
            '/dcm.in'
        )
        self.assertEqual(expected, create_transfer_command(mt))
