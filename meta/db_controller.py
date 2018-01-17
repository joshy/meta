import datetime
from sqlalchemy.dialects.postgresql import JSON

REGISTERED = 'creation_time'
STARTED = 'started'
FINISHED = 'finished'


def download_status():
    """ Returns all done tasks and open tasks as lists.
    A task is a named tuple.
    """
    return

    queued_task_ids = db.smembers(REGISTERED)
    finished_task_ids = db.smembers(FINISHED)

    queued_tasks = [db.hgetall(task) for task in queued_task_ids]
    finished_tasks = [db.hgetall(task) for task in finished_task_ids]

    return queued_tasks, finished_tasks


def change_task_status(db, task_id, status, exception=''):
    db.smove(REGISTERED, FINISHED, task_id)

    start_time_string = str(
        db.hmget(task_id, STARTED)[0]
    )

    start_time = datetime.datetime.strptime(
        start_time_string,
        "%Y-%m-%d %H:%M:%S.%f"
    )

    running_time = datetime.datetime.now() - start_time

    db.hmset(
        task_id,
        {
            FINISHED: str(datetime.datetime.now()),
            'running_time': str(running_time),
            'status': status,  # TODO: get from celery_app
            'exception': exception
        }
    )


def flush(db):
    print("++++ PRETENDING TO FLUSH")
    # db.flushall()
    # TODO Clear all from Celery as well



def store_task_start_time(task_id):
    db.hmset(
        task_id,
        {
            STARTED: str(datetime.datetime.now())
        }
    )