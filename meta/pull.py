import subprocess
import shlex
import os

from concurrent.futures import ThreadPoolExecutor

from meta.command_creator import transfer_command
from meta.task import transfer_task, finish_task, select_transfer
from meta.app import app

POOL = ThreadPoolExecutor(1)


def get_db():
    raise NotImplementedError('If you can see this it means the legacy code is still running')


def transfer_status():
    transfers = select_transfer(get_db())
    waiting = [t for t in transfers if t['status'] is None]
    done = [t for t in transfers if t['status'] is not None]
    return waiting, done


def _task_done(future):
    with app.app_context():
        finish_task(get_db(), future)


def transfer_series(command, series_list, target):
    """ Transfer the series to target PACS node. """
    study_id_list = [entry['study_id'] for entry in series_list]
    study_ids = set(study_id_list)
    app.logger.debug('Transferring ids: %s', study_ids)

    for study_id in study_ids:
        raise NotImplementedError

        command = transfer_command(DCMTK_CONFIG, PACS_CONFIG, target, study_id)
        args = shlex.split(command)
        app.logger.debug('Running args %s', args)
        future = POOL.submit(subprocess.run, args,
                             stderr=subprocess.PIPE, shell=False)
        future.task = transfer_task(get_db(), study_id)
        future.add_done_callback(_task_done)
    return len(study_ids)



