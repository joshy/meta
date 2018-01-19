from datetime import datetime
import shlex
import subprocess
from meta.queue_manager_models import TaskInfo
from concurrent.futures import ThreadPoolExecutor
from meta.queue_manager_models import db
import traceback

_executor = ThreadPoolExecutor(1)
_global_task_id = None


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


def _bash_task(app, task_id, args):
    app.app_context().push()
    global _global_task_id
    _global_task_id = task_id

    print('+++++ TASK ID', task_id, db)
    
    task_info = TaskInfo.query.get(task_id)
    task_info.started = datetime.now()
    task_info.status = 'SUBMITTED'
    db.session.commit()

    # TODO: UNCOMMENT THIS FOR PRODUCTION!
    #output = subprocess.run(args, stderr=subprocess.PIPE, shell=False)


def _task_finished_callback(future):
    status = 'SUCCEEDED'
    exception = None

    e = future.exception()
    if e:
        status = 'FAILED'
        exception = traceback.format_exc()

    task_info = TaskInfo.query.get(_global_task_id)
    task_info.flag_finished = True
    task_info.finished = datetime.now()
    if task_info.started:
        task_info.running_time = task_info.finished - task_info.started
    task_info.status = status
    task_info.exception = exception

    db.session.commit()


def submit_task(app, dir_name, entry, command):
    task_id = _store_task_info(dir_name, entry, command)

    args = shlex.split(command)

    app.logger.debug('Running args %s', args)

    task_info = TaskInfo.query.get(task_id)
    task_info.status = 'SUBMITTING'
    db.session.commit()

    future = _executor.submit(_bash_task, app, task_id, args)
    future.add_done_callback(_task_finished_callback)


def _retry_tasks(app, tasks, coerce_retry=False):
    retry_status = 'RETRY'

    if not len(tasks):
        return

    if _executor._work_queue.qsize() and not coerce_retry:
        return

    for task in tasks:
        retry_counter = 0
        if retry_status in task.status:
            retry_counter = int(task.status[len(retry_status):])
        retry_counter += 1
        task.status = '{}{}'.format(retry_status, retry_counter)

        db.session.commit()

        args = shlex.split(task.command)

        task = _executor.submit(_bash_task, app, task.id, args)
        task.add_done_callback(_task_finished_callback)


def task_status(app, task_type):
    """ Returns all done tasks and open tasks.
    """
    unfinished_tasks = (
        TaskInfo.query
        .filter(~TaskInfo.flag_finished)
        .filter(TaskInfo.type == task_type)
        .order_by(TaskInfo.creation_time.desc())
        .all()
    )

    _retry_tasks(app, unfinished_tasks)

    finished_tasks = (
        TaskInfo.query
        .filter(TaskInfo.flag_finished)
        .filter(TaskInfo.type == task_type)
        .order_by(TaskInfo.finished)
        .all()
    )

    return unfinished_tasks, finished_tasks
