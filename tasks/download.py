import logging
import os

import luigi
from luigi.contrib.external_program import ExternalProgramTask

import shlex

class DownloadTask(luigi.contrib.external_program.ExternalProgramTask):

    command = luigi.Parameter()

    def program_args(self):
        return shlex.split(self.command)
