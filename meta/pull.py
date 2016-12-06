import subprocess, shlex
import os

from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from meta.settings import OUTPUT_DIR
from meta.command import base_command, transfer_command
from meta.app import app

Task = namedtuple('Tasks', ['patient_id', 'accession_number', 'series_number',
                            'creation_time', 'status', 'exception'])

POOL = ThreadPoolExecutor(1)
FUTURES = []

def status():
    """ Returns all done tasks and open tasks as lists.
    A task is a named tuple.
    """
    done_tasks = [future.task for future in FUTURES if future.done()]
    waiting_tasks = [future.task for future in FUTURES if not future.done()]
    return (waiting_tasks, done_tasks)


def _download_done(future):
    future.task = future.task._replace(
        exception=future.exception(),
        status='Successful' if future.exception() is None else 'Error')


def download_series(series_list, dir_name):
    """ Download the series. The folder structure is as follows:
        MAIN_DOWNLOAD_DIR / USER_DEFINED / PATIENTID / ACCESSION_NUMBER /
          / SERIES_NUMER
    """

    for entry in series_list:
        image_folder = _create_image_dir(entry, dir_name)
        patient_id = entry['patient_id']
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        accession_number = entry['accession_number']
        series_number = entry['series_number']
        command = base_command() \
                  + ' --output-directory ' + image_folder \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid
        args = shlex.split(command)
        app.logger.debug('Running args %s', args)
        future = POOL.submit(subprocess.run, args, shell=False)
        future.task = Task(patient_id=patient_id,
                           accession_number=accession_number,
                           series_number=series_number,
                           creation_time=str(datetime.now()),
                           status=None,
                           exception=None)
        future.add_done_callback(_download_done)
        FUTURES.append(future)


def transfer_series(series_list, target):
    """ Transfer the series to target PACS node. """
    study_id_list = [entry['study_id'] for entry in series_list]
    study_ids = set(study_id_list)
    app.logger.debug('Transferring ids: %s', study_ids)

    for study_id in study_ids:
        command = transfer_command(target) \
                  + ' -k StudyInstanceUID=' + study_id
        args = shlex.split(command)
        app.logger.debug('Running args %s', args)
        future = POOL.submit(subprocess.run, args, shell=False)
        FUTURES.append(future)


def _create_image_dir(entry, dir_name):
    patient_id = entry['patient_id']
    accession_number = entry['accession_number']
    series_number = entry['series_number']
    image_folder = os.path.join(OUTPUT_DIR, dir_name, patient_id,
                                accession_number, series_number)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder, exist_ok=True)
    return image_folder
