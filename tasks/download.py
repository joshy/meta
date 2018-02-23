import luigi
from luigi.contrib.external_program import ExternalProgramTask
import shlex
from os.path import join, exists
from os import makedirs
import subprocess


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

    # luigi input args
    patient_id = luigi.Parameter()
    accession_number = luigi.Parameter()
    series_number = luigi.Parameter()

    study_instance_uid = luigi.Parameter()
    series_instance_uid = luigi.Parameter()

    dir_name = luigi.Parameter()


    resources = { 'pacs': 1}
    max_batch_size = 1

    def get_image_dir(self):
        return join(self.output_dir, self.dir_name, self.patient_id, self.accession_number, self.series_number)

    def program_args(self):
        base_command = (
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

        image_dir = self.get_image_dir()
        if not exists(image_dir):
            makedirs(image_dir, exist_ok=True)

        command = (
            base_command +
            ' --output-directory ' + image_dir +
            ' -k StudyInstanceUID=' + self.study_instance_uid +
            ' -k SeriesInstanceUID=' + self.series_instance_uid +
            ' ' + self.dcmin
        )
        return shlex.split(command)
