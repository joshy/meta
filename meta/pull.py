import collections
import subprocess
import os
import time
import threading
import random

from concurrent.futures import ThreadPoolExecutor

from meta.settings import OUTPUT_DIR
from meta.command import BASE_COMMAND, transfer_command
from meta.app import app

POOL = ThreadPoolExecutor(1)
FUTURES = []
Status = collections.namedtuple('Status', ['total', 'running', 'done'])

def status():
    """ Returns the status on all running tasks. """
    running = [task for task in FUTURES if task.running()]
    done = [task for task in FUTURES if task.done()]
    return Status(total=len(FUTURES), running=len(running), done=len(done))


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
        command = BASE_COMMAND \
                  + ' --output-directory ' + image_folder \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid
        app.logger.debug('Running command %s', command)
        FUTURES.append(POOL.submit(command, ()))


def transfer_series(series_list, target):
    """ Transfer the series to target PACS node. """
    study_id_list = [entry['study_id'] for entry in series_list]
    study_ids = set(study_id_list)
    app.logger.debug('Transferring ids: %s', study_ids)

    for study_id in study_ids:
        command = transfer_command(target) \
                  + ' -k StudyInstanceUID=' + study_id
        app.logger.debug('Running command %s', command)
        FUTURES.append(POOL.submit(command, ()))
