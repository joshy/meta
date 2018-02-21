import luigi
from luigi.contrib.external_program import ExternalProgramTask


class MoveTask(luigi.contrib.external_program.ExternalProgramTask):
    study_id = luigi.Parameter()
    aet = luigi.Parameter()
    aec = luigi.Parameter()
    aem = luigi.Parameter()
    peer_address = luigi.Parameter()
    peer_port = luigi.Parameter()
    incoming_port = luigi.Parameter()
    dcmin = luigi.Parameter()
    movescu = luigi.Parameter()

    def program_args(self):
        ids = 'StudyInstanceUID={}'.format(self.study_id)
        x = [self.movescu, '-v', '-S', '-aem', self.aem,
             '-aet', self.aet, '-aec', self.aec, self.peer_address,
             self.peer_port, '+P', self.incoming_port, '-k', ids, self.dcmin
        ]
        return x

    def run(self):
        #super().run()
        with self.output().open('w') as output:
            output.write('Done')

    def output(self):
        name = str(self.study_id).rstrip() + '.run_success'
        return luigi.LocalTarget(name)

