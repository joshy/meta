import luigi
from luigi.contrib.external_program import ExternalProgramTask
import shlex
from os.path import join, exists
from os import makedirs
import subprocess


class DownloadTask(luigi.contrib.external_program.ExternalProgramTask):
    # loaded from cfg
    dcmin = luigi.Parameter(default='')
    movescu = luigi.Parameter(default='')
    aet = luigi.Parameter(default='')
    aec = luigi.Parameter(default='')
    peer_address = luigi.Parameter(default='')
    peer_port = luigi.Parameter(default='')
    incoming_port = luigi.Parameter(default='')
    output_dir = luigi.Parameter(default='')

    # luigi inputs
    patient_id = luigi.Parameter(default='')
    accession_number = luigi.Parameter(default='')
    series_number = luigi.Parameter(default='')
    study_instance_uid = luigi.Parameter(default='')
    series_instance_uid = luigi.Parameter(default='')
    dir_name = luigi.Parameter(default='')

    resources = {'pacs': 1}
    max_batch_size = 1

    def get_image_dir(self):
        return join(
            self.output_dir,
            self.dir_name,
            self.patient_id,
            self.accession_number,
            self.series_number
        )

    def get_base_command(self):
        return (
            '{} -v -S -k QueryRetrieveLevel=SERIES -aet {} -aec {} {} {} +P {}'
            .format(
                self.movescu,
                self.aet,
                self.aec,
                self.peer_address,
                self.peer_port,
                self.incoming_port
            )
        )

    def get_command(self, base_command, image_dir):
        return (
            base_command +
            ' --output-directory ' + image_dir +
            ' -k StudyInstanceUID=' + self.study_instance_uid +
            ' -k SeriesInstanceUID=' + self.series_instance_uid +
            ' ' + self.dcmin
        )

    def program_args(self):
        base_command = self.get_base_command()

        image_dir = self.get_image_dir()

        if not exists(image_dir):
            makedirs(image_dir, exist_ok=True)

        command = self.get_command(base_command, image_dir)

        return shlex.split(command)
