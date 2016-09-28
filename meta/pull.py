import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor as Pool

from meta.settings import *


def callback(future):
    if future.exception is not None:
        logging.warning('Got Exception: %s', future.exception)
    else:
        logging.info('Download done')


def download(series_list):
    for entry in series_list:
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        command = BASE_COMMAND + ' --output-directory ' \
                  + OUTPUT_DIR \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid
        logging.debug('Running command %s', command)
        pool = Pool(max_workers=1)
        f = pool.submit(subprocess.call, command, shell=True)
        f.add_done_callback(callback)
        subprocess.call(command, shell=True)


def transfer(series_list):
    for entry in series_list:
        study_instance_uid = entry['study_id']
        series_instance_uid = entry['series_id']
        command = BASE_COMMAND + ' --output-directory ' \
                  + OUTPUT_DIR \
                  + ' -k StudyInstanceUID=' + study_instance_uid \
                  + ' -k SeriesInstanceUID=' + series_instance_uid
        logging.debug('Running command %s', command)
        pool = Pool(max_workers=1)
        f = pool.submit(subprocess.call, command, shell=True)
        f.add_done_callback(callback)
        subprocess.call(command, shell=True)
