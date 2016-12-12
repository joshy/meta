import subprocess
import shlex
import os

from concurrent.futures import ThreadPoolExecutor, Future

from meta.settings import OUTPUT_DIR
from meta.command import base_command, transfer_command
from meta.task import create_download_task, finish_download_task
from meta.app import app


POOL = ThreadPoolExecutor(1)
FUTURES_WAITING = []  # type: List[Future]
FUTURES_DONE = []  # type: List[Future]


def status():
    """ Returns all done tasks and open tasks as lists.
    A task is a named tuple.
    """
    done_tasks = [future.task for future in FUTURES_WAITING]
    waiting_tasks = [future.task for future in FUTURES_DONE]
    return (waiting_tasks, done_tasks)


def _download_done(future):
    future.task = finish_download_task(future)
    FUTURES_WAITING.pop(future)
    FUTURES_DONE.append(future)


def download_series(series_list, dir_name):
    """ Download the series. The folder structure is as follows:
        MAIN_DOWNLOAD_DIR / USER_DEFINED / PATIENTID / ACCESSION_NUMBER /
          / SERIES_NUMER
    """

    for entry in series_list:
        image_folder = _create_image_dir(entry, dir_name)
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        command = base_command() \
                  + ' --output-directory ' + image_folder \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid
        args = shlex.split(command)
        app.logger.debug('Running args %s', args)
        future = POOL.submit(subprocess.run, args, shell=False)
        future.task = create_download_task(entry)
        future.add_done_callback(_download_done)
        FUTURES_WAITING.append(future)


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
        FUTURES_WAITING.append(future)


def _create_image_dir(entry, dir_name):
    patient_id = entry['patient_id']
    accession_number = entry['accession_number']
    series_number = entry['series_number']
    image_folder = os.path.join(OUTPUT_DIR, dir_name, patient_id,
                                accession_number, series_number)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder, exist_ok=True)
    return image_folder
