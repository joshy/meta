from datetime import datetime
import shlex
from subprocess import run, PIPE
from meta.models import TaskInfo
from concurrent.futures import ThreadPoolExecutor
from meta.models import db
import traceback
from functools import partial
from flask import current_app

_executor = ThreadPoolExecutor(1)


def flush_db():
    TaskInfo.query.delete()
    db.session.commit()


def _store_task_info(dir_name, entry, command):
    task_info = TaskInfo(
        dir_name=dir_name,
        study_id=entry.get('study_id'),
        patient_id=entry.get('patient_id'),
        accession_number=entry.get('accession_number'),
        series_number=entry.get('series_number'),
        command=command,
        running_time=None,
        status='REGISTERED',
        exception=None,
        started=None,
        finished=None,
        flag_finished=False,
        type=entry['type']
    )
    db.session.add(task_info)
    db.session.commit()

    return task_info.id


def _bash_task(task_id, config, args):
    from meta.app_creator import create_app

    create_app(db_uri=config['SQLALCHEMY_DATABASE_URI'],
               testing=config['TESTING'],
               server_name=config['SERVER_NAME'])
    task_info = TaskInfo.query.get(task_id)
    task_info.started = datetime.now()
    task_info.status = 'RUNNING'
    db.session.commit()
    run(args, stderr=PIPE, shell=False, check=True)


def _task_finished_callback(future, task_id):
    status = 'SUCCEEDED'
    exception = None

    e = future.exception()
    if e:
        status = 'FAILED'
        exception = traceback.format_exc()

    task_info = TaskInfo.query.get(task_id)
    task_info.flag_finished = True
    task_info.finished = datetime.now()
    if task_info.started:
        task_info.running_time = task_info.finished - task_info.started
    task_info.status = status
    task_info.exception = exception

    db.session.commit()


def submit_task(dir_name, entry, command):
    task_id = _store_task_info(dir_name, entry, command)
    args = shlex.split(command)
    current_app.logger.debug('Running args %s', args)
    future = _executor.submit(_bash_task, task_id, current_app.config, args)
    callback_fun = partial(_task_finished_callback, task_id=task_id)
    future.add_done_callback(callback_fun)

    return task_id


def _retry_tasks(tasks):
    retry_status = 'RETRY'

    if not len(tasks):
        return

    if _executor._work_queue.unfinished_tasks > 0:
        return

    for task in tasks:
        retry_counter = 0
        if retry_status in task.status:
            retry_counter = int(task.status[len(retry_status):])
        retry_counter += 1
        task.status = '{}{}'.format(retry_status, retry_counter)

        db.session.commit()

        args = shlex.split(task.command)
        future = _executor.submit(_bash_task, task.id, current_app.config, args)
        callback_fun = partial(_task_finished_callback, task_id=task.id)
        future.add_done_callback(callback_fun)


def task_status(task_type):
    """ Returns all done tasks and open tasks.
    """
    unfinished_tasks = (
        TaskInfo.query
        .filter(~TaskInfo.flag_finished)
        .filter(TaskInfo.type == task_type)
        .order_by(TaskInfo.creation_time.desc())
        .limit(10000)
        .all()
    )

    _retry_tasks(unfinished_tasks)

    finished_tasks = (
        TaskInfo.query
        .filter(TaskInfo.flag_finished)
        .filter(TaskInfo.type == task_type)
        .order_by(TaskInfo.finished.desc())
        .limit(10000)
        .all()
    )

    return unfinished_tasks, finished_tasks
