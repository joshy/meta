import shlex

import luigi
from luigi.contrib.external_program import ExternalProgramTask

from tasks.command import create_download_command


class DownloadTask(luigi.contrib.external_program.ExternalProgramTask):
    # loaded from cfg
    dcmin = luigi.Parameter()
    movescu = luigi.Parameter()
    aet = luigi.Parameter()
    aec = luigi.Parameter()
    peer_address = luigi.Parameter()
    peer_port = luigi.Parameter()
    incoming_port = luigi.Parameter()
    output_dir = luigi.Parameter()

    # luigi inputs
    patient_id = luigi.Parameter()
    accession_number = luigi.Parameter()
    series_number = luigi.Parameter()
    study_instance_uid = luigi.Parameter()
    series_instance_uid = luigi.Parameter()
    dir_name = luigi.Parameter()

    resources = {'pacs': 1}
    max_batch_size = 1


    def program_args(self):
        command = create_download_command(self)
        return shlex.split(command)
