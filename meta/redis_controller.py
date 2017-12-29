from redis import Redis
import datetime

REGISTERED = 'creation_time'
STARTED = 'started'
FINISHED = 'finished'

redis_db = Redis('localhost', decode_responses=True)


def download_status():
    """ Returns all done tasks and open tasks as lists.
    A task is a named tuple.
    """
    queued_task_ids = redis_db.smembers(REGISTERED)
    finished_task_ids = redis_db.smembers(FINISHED)

    queued_tasks = [redis_db.hgetall(task) for task in queued_task_ids]
    finished_tasks = [redis_db.hgetall(task) for task in finished_task_ids]

    return queued_tasks, finished_tasks


def change_task_status(task_id, status, exception=''):
    redis_db.smove(REGISTERED, FINISHED, task_id)

    start_time_string = str(
        redis_db.hmget(task_id, STARTED)[0]
    )

    start_time = datetime.datetime.strptime(
        start_time_string,
        "%Y-%m-%d %H:%M:%S.%f"
    )

    running_time = datetime.datetime.now() - start_time

    redis_db.hmset(
        task_id,
        {
            FINISHED: str(datetime.datetime.now()),
            'running_time': str(running_time),
            'status': status,  # TODO: get from celery
            'exception': exception
        }
    )


def flush():
    redis_db.flushall()
    # TODO Clear all from Celery as well


def store_task_info(task_id, dir_name, entry, command):
    redis_db.hmset(
        task_id,
        {
            'dir_name': dir_name,
            'patient_id': entry['patient_id'],
            'accession_number': entry['accession_number'],
            'series_number': entry['series_number'],
            'command': command,
            REGISTERED: str(datetime.datetime.now())
        }
    )


def store_task_registered_time(task_id):
    redis_db.sadd(REGISTERED, task_id)


def store_task_start_time(task_id):
    redis_db.hmset(
        task_id,
        {
            STARTED: str(datetime.datetime.now())
        }
    )