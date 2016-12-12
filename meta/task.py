from collections import namedtuple
from datetime import datetime
from typing import Dict

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
Task = namedtuple('Tasks', ['patient_id', 'accession_number', 'series_number',
                            'creation_time', 'execution_time', 'running_time',
                            'status', 'exception'])


def create_download_task(entry: Dict[str, str]) -> Task:
    """
    Creates a new download task with all the necessary fields set.
    """
    patient_id = entry['patient_id']
    accession_number = entry['accession_number']
    series_number = entry['series_number']

    return Task(patient_id=patient_id,
                accession_number=accession_number,
                series_number=series_number,
                creation_time=str(datetime.now()),
                execution_time=str(datetime.now()),
                running_time="0",
                status=None,
                exception=None)


def finish_download_task(future):
    """
    Returns a new task with calculated execution times.
    """
    return future.task._replace(
        execution_time=str(datetime.now),
        running_time=_calculate_running_time(future.task),
        exception=future.exception(),
        status='Successful' if future.exception() is None else 'Error')


def _calculate_running_time(task):
    end = datetime.strptime(task.execution_time, DATE_FORMAT)
    start = datetime.strptime(task.creation_time, DATE_FORMAT)
    delta = end-start
    return str(delta)
