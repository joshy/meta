import shlex

import luigi
from luigi.contrib.external_program import ExternalProgramTask
from tasks.command import create_transfer_command


class MoveTask(luigi.contrib.external_program.ExternalProgramTask):
    # loaded from cfg
    dcmin = luigi.Parameter()
    movescu = luigi.Parameter()
    aet = luigi.Parameter()
    aec = luigi.Parameter()
    peer_address = luigi.Parameter()
    peer_port = luigi.Parameter()
    incoming_port = luigi.Parameter()

    # luigi inputs
    series_instance_uid = luigi.Parameter()
    target = luigi.Parameter()


    def program_args(self):
        command = create_transfer_command(self)
        return shlex.split(command)
