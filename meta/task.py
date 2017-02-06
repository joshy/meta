from collections import namedtuple
from datetime import datetime
from typing import Dict

from meta.tasks_db import insert_download

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
Task = namedtuple('Tasks', ['patient_id', 'accession_number', 'series_number',
                            'creation_time', 'execution_time', 'running_time',
                            'dir_name', 'status', 'exception'])

TransferTask = namedtuple('TransferTask',
                          ['study_id', 'creation_time', 'execution_time',
                           'running_time', 'status', 'exception'])


def download_task(cursor, entry: Dict[str, str], dir_name: str) -> Task:
    """
    Creates a new download task with all the necessary fields set.
    """
    patient_id = entry['patient_id']
    accession_number = entry['accession_number']
    series_number = entry['series_number']

    task = Task(patient_id=patient_id,
                accession_number=accession_number,
                series_number=series_number,
                dir_name=dir_name,
                creation_time=str(datetime.now()),
                execution_time=str(datetime.now()),
                running_time="0",
                status=None,
                exception=None)
    insert_download(cursor, task)
    return task


def finish_task(future):
    """
    Returns a new task with calculated execution times.
    """
    return future.task._replace(
        execution_time=str(datetime.now),
        running_time=_calculate_running_time(future.task),
        exception=future.exception(),
        status='Successful' if future.exception() is None else 'Error')


def transfer_task(study_id) -> TransferTask:
    """
    Creates a new transfer task with all the necessary fields set.
    """
    return TransferTask(study_id=study_id,
                        creation_time=str(datetime.now()),
                        execution_time=str(datetime.now()),
                        running_time="0",
                        status=None,
                        exception=None)


def _calculate_running_time(task):
    end = datetime.strptime(task.execution_time, DATE_FORMAT)
    start = datetime.strptime(task.creation_time, DATE_FORMAT)
    delta = end-start
    return str(delta)
