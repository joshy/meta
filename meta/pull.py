import subprocess
import os

from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor

from meta.settings import OUTPUT_DIR
from meta.command import BASE_COMMAND, transfer_command
from meta.app import app

Status = namedtuple('Status', ['total', 'running', 'done'])
Task = namedtuple('Tasks', ['accession_number', 'series_number', 'status',
                            'exception'])

POOL = ThreadPoolExecutor(1)
FUTURES = []
DONE_TASKS = []

def status():
    """ Returns all done tasks. """
    return DONE_TASKS


def download_done(future):
    task = Task(accession_number=future.accession_number,
                series_number=future.series_number,
                exception=future.exception(),
                status='Successful' if future.exception() is None else 'Error')
    DONE_TASKS.append(task)


def download_series(series_list, dir_name):
    """ Download the series. """
    image_folder = os.path.join(os.getcwd(), OUTPUT_DIR, dir_name)

    if not os.path.exists(image_folder):
        app.logger.debug(
            "Folder {} does not exists, creating it".format(image_folder))
        os.makedirs(image_folder)

    for entry in series_list:
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        accession_number = entry['accession_number']
        series_number = entry['series_number']
        command = BASE_COMMAND \
                  + ' --output-directory ' + image_folder \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid
        app.logger.debug('Running command %s', command)
        future = POOL.submit(subprocess.call, command, shell=False)
        future.accession_number = accession_number
        future.series_number = series_number
        future.add_done_callback(download_done)
        FUTURES.append(future)


def transfer_series(series_list, target):
    """ Transfer the series to target PACS node. """
    study_id_list = [entry['study_id'] for entry in series_list]
    study_ids = set(study_id_list)
    app.logger.debug('Transferring ids: %s', study_ids)

    for study_id in study_ids:
        command = transfer_command(target) \
                  + ' -k StudyInstanceUID=' + study_id
        app.logger.debug('Running command %s', command)
        future = POOL.submit(subprocess.call, command, shell=False)
        FUTURES.append(future)
