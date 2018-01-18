from datetime import datetime
import time
import shlex
import subprocess
from meta.queue_manager_models import TaskInfo
from meta.queue_manager_db import db
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(1)


def _store_task_info(dir_name, entry, command):
    # TODO: If there was no Flask related inheritance, we could use in-db inheritance
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


def _bash_task(task_id, args):
    # TODO: needs to get connection to db
    print('++++++ IN THREAD: ', db)

    task_info = TaskInfo.query.get(task_id)
    task_info.started = datetime.now()
    task_info.status = 'SUBMITTED'

    db.session.commit()

    try:
        # TODO: UNCOMMENT THIS FOR PRODUCTION!
        #output = subprocess.run(args, stderr=subprocess.PIPE, shell=False)
        time.sleep(5)
        raise ValueError

        task_info.status = 'SUCCEEDED'
        print('+++ SUCCESS', task_id)
    except:
        task_info.status = 'FAILED'
        task_info.exception = '{}{}{}'.format(*sys.exc_info())
        print('+++ FAIL', task_id)
    finally:
        print('+++ FLAGGED FINISHED')
        task_info.flag_finished = True
        task_info.finished = datetime.now()
        if task_info.started:
            task_info.running_time = task_info.finished - task_info.started
        db.session.commit()

    # TODO: Delete this
    print('+++ FINISHED', task_id)

    return output


def submit_task(dir_name, entry, command):

    task_id = _store_task_info(dir_name, entry, command)
    print("++++ QUEUE TASK", task_id)

    args = shlex.split(command)

    # TODO: handle logger
    #app.logger.debug('Running args %s', args)

    print('++++ SUBMITTING TASK', task_id)
    task_info = TaskInfo.query.get(task_id)
    task_info.status = 'SUBMITTING'
    db.session.commit()

    print('BEFORE THREAD', db)
    executor.submit(_bash_task, task_id, args)

    return task_id


def _retry_tasks(tasks, coerce_retry=False):
    RETRY = 'RETRY'

    print('+++ PENDING:', executor._work_queue.qsize(), type(executor._work_queue.qsize()))
    print('+++ THREADS:', executor._threads)

    if not len(tasks):
        print('+++ No tasks to clean up :D')
        return

    if executor._work_queue.qsize() and not coerce_retry:
        print('+++ still something queued, skipping cleaning up (and retry not coerced)')
        return

    for task in tasks:
        retry_counter = 0
        if RETRY in task.status:
            retry_counter = int(task.status[len(RETRY):])
        retry_counter += 1
        task.status = '{}{}'.format(RETRY, retry_counter)

        db.session.commit()

        args = shlex.split(task.command)

        executor.submit(_bash_task, task.id, args)


def task_status(task_type):
    """ Returns all done tasks and open tasks as lists.
    A task is a named tuple.
    """
    unfinished_tasks = (
        TaskInfo.query
        .filter(~TaskInfo.flag_finished)
        .filter(TaskInfo.type == task_type)
        .order_by(TaskInfo.creation_time.desc())
        .all()
    )

    _retry_tasks(unfinished_tasks)

    finished_tasks = (
        TaskInfo.query
        .filter(TaskInfo.flag_finished)
        .filter(TaskInfo.type == task_type)
        .order_by(TaskInfo.finished)
        .all()
    )

    print('+++   FINISHED TASKS LEN: ', len(finished_tasks))
    print('+++ UNFINISHED TASKS LEN: ', len(unfinished_tasks))

    return unfinished_tasks, finished_tasks


