import subprocess

from meta.settings import *
from meta import app

def download(series_list):
    for entry in series_list:
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        command = BASE_COMMAND + ' --output-directory ' \
                  + OUTPUT_DIR \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid
        app.logger.debug('Running command %s', command)
        subprocess.call(command, shell=True)


def transfer(series_list):
    for entry in series_list:
        study_instance_uid = entry['study_id']
        command = TRANSFER_COMMAND \
                  + ' -k StudyInstanceUID=' + study_instance_uid
        app.logger.debug('Running command %s', command)
        subprocess.call(command, shell=True)
