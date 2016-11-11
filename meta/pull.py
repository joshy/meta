import subprocess
import os

from meta.settings import OUTPUT_DIR
from meta.command import BASE_COMMAND, transfer_command
from meta import app


def download(series_list, dir_name):
    image_folder = os.path.join(os.getcwd(), OUTPUT_DIR, dir_name)

    if not os.path.exists(image_folder):
        app.logger.debug(
            "Folder {0} does not exists, creating it".format(image_folder))
        os.makedirs(image_folder)

    for entry in series_list:
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        command = BASE_COMMAND \
                  + ' --output-directory ' + image_folder \
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
