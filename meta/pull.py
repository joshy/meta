import subprocess

from meta.settings import OUTPUT_DIR
from meta.command import *
from meta import app


def download(series_list):
    for entry in series_list:
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        command = BASE_COMMAND \
                  + ' --output-directory ' + OUTPUT_DIR \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid
        app.logger.debug('Running command %s', command)
        subprocess.call(command, shell=True)


def transfer(series_list, target):
    study_id_list = [entry['study_id'] for entry in series_list]
    study_ids = set(study_id_list)
    app.logger.debug('Transferring ids: %s', study_ids)

    for study_id in study_ids:
        command = transfer_command(target) \
                  + ' -k StudyInstanceUID=' + study_id
        app.logger.debug('Running command %s', command)
        subprocess.call(command, shell=True)
