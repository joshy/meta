import unittest
from meta.command_creator import construct_transfer_command
from tasks.download import DownloadTask
from meta.config import dcmtk_config, pacs_config
from unittest.mock import patch

DCMTK_CONFIG = dcmtk_config({'DCMTK_BIN':'/usr/local/bin/',
                             'DCMIN': '/opt/dcm.in'})

PACS_CONFIG = pacs_config({'AE_TITLE':'AE_TITLE', 'AE_CALLED': 'AE_CALLED',
                           'PEER_ADDRESS': '127.0.0.1', 'PEER_PORT': 104,
                           'INCOMING_PORT': 11110})


class TestCommand(unittest.TestCase):
    def test_base_command(self):
        expected = (
            '/usr/local/bin/movescu '
            '-v -S -k QueryRetrieveLevel=SERIES '
            '-aet AE_TITLE '
            '-aec AE_CALLED '
            '127.0.0.1 104 +P 11110'
        )

        dt = DownloadTask()

        dt.movescu = '/usr/local/bin/movescu'
        dt.aet = 'AE_TITLE'
        dt.aec = 'AE_CALLED'
        dt.peer_address = '127.0.0.1'
        dt.peer_port = '104'
        dt.incoming_port = '11110'

        self.assertEqual(expected, dt.get_base_command())

    def test_image_dir(self):
        expected = '/output_dir/dir_name/patient_id/accession_number/series_number'

        dt = DownloadTask()

        dt.output_dir = '/output_dir'
        dt.dir_name = 'dir_name'
        dt.patient_id = 'patient_id'
        dt.accession_number = 'accession_number'
        dt.series_number = 'series_number'

        self.assertEqual(expected, dt.get_image_dir())

    def test_get_command(self):
        with patch('tasks.download.makedirs') as mock_makedirs:
            mock_makedirs.return_value = None

            dt = DownloadTask()

            dt.study_instance_uid = 'study_instance_uid'
            dt.series_instance_uid  = 'series_instance_uid'
            dt.dcmin = 'dcmin'

            expected = ('base_command '
                        '--output-directory image_dir '
                        '-k StudyInstanceUID=study_instance_uid '
                        '-k SeriesInstanceUID=series_instance_uid dcmin')

            self.assertEqual(expected, dt.get_command('base_command', 'image_dir'))

    def test_transfer(self):
        expected = (
            '/usr/local/bin/movescu '
            '-v -S -aem SRSYVMS01 '
            '-aet AE_TITLE '
            '-aec AE_CALLED '
            '127.0.0.1 104 +P 11110 '
            '-k StudyInstanceUID=12345 '
            '/opt/dcm.in'
        )
        self.assertEqual(expected, construct_transfer_command(DCMTK_CONFIG, PACS_CONFIG, 'syngo', '12345'))
