import subprocess
import shlex
import os

from concurrent.futures import ThreadPoolExecutor, Future

from meta.command import base_command, transfer_command
from meta.task import download_task, transfer_task, finish_task, select_download, select_transfer
from meta.app import app, OUTPUT_DIR, DCMTK_CONFIG, PACS_CONFIG, get_db

POOL = ThreadPoolExecutor(1)


def transfer_status():
    transfers = select_transfer(get_db())
    waiting = [t for t in transfers if t['status'] is None]
    done = [t for t in transfers if t['status'] is not None]
    return (waiting, done)


def download_status():
    """ Returns all done tasks and open tasks as lists.
    A task is a named tuple.
    """
    downloads = select_download(get_db())
    waiting = [t for t in downloads if t['status'] is None]
    done = [t for t in downloads if t['status'] is not None]
    return (waiting, done)


def _task_done(future):
    with app.app_context():
        finish_task(get_db(), future)


def download_series(series_list, dir_name):
    """ Download the series. The folder structure is as follows:
        MAIN_DOWNLOAD_DIR / USER_DEFINED / PATIENTID / ACCESSION_NUMBER /
          / SERIES_NUMER
    """

    for entry in series_list:
        image_folder = _create_image_dir(entry, dir_name)
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        command = base_command(DCMTK_CONFIG, PACS_CONFIG) \
                  + ' --output-directory ' + image_folder \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid \
                  + ' ' + DCMTK_CONFIG.dcmin
        args = shlex.split(command)
        app.logger.debug('Running args %s', args)
        future = POOL.submit(subprocess.run, args, shell=False)
        future.task = download_task(get_db(), entry, dir_name)
        future.add_done_callback(_task_done)
    return len(series_list)


def transfer_series(series_list, target):
    """ Transfer the series to target PACS node. """
    study_id_list = [entry['study_id'] for entry in series_list]
    study_ids = set(study_id_list)
    app.logger.debug('Transferring ids: %s', study_ids)

    for study_id in study_ids:
        command = transfer_command(DCMTK_CONFIG, PACS_CONFIG, target, study_id)
        args = shlex.split(command)
        app.logger.debug('Running args %s', args)
        future = POOL.submit(subprocess.run, args, shell=False)
        future.task = transfer_task(get_db(), study_id)
        future.add_done_callback(_task_done)
    return len(study_ids)


def _create_image_dir(entry, dir_name):
    patient_id = entry['patient_id']
    accession_number = entry['accession_number']
    series_number = entry['series_number']
    image_folder = os.path.join(OUTPUT_DIR, dir_name, patient_id,
                                accession_number, series_number)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder, exist_ok=True)
    return image_folder
