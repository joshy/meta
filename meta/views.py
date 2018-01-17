import json
from requests import get, RequestException
from flask import render_template, request

from meta.app import app, VERSION, DEMO, RESULT_LIMIT, REPORT_SHOW_URL
from meta.app import OUTPUT_DIR, DCMTK_CONFIG, PACS_CONFIG

from meta.query import query_body
from meta.paging import calc
from meta.facets import prepare_facets
from meta.grouping import group
from meta.solr import solr_url
from meta.terms import get_terms_data

#from meta.db_controller import download_status, flush
from meta.pull import transfer_series, transfer_status

from celery import Celery
from celery.signals import task_success, task_failure, task_postrun

import shlex
import subprocess

from meta.command_creator import construct_download_command

# import meta.db_controller as dbc

from flask_sqlalchemy import SQLAlchemy

import time
from datetime import datetime


def make_celery(flask_app):

    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config['CELERY_BROKER_URL']
    )

    celery_app.conf.update(flask_app.config)
    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery_app = make_celery(app)
db = SQLAlchemy(app)


class TaskInfo(db.Model):
    __tablename__ = 'task_info'

    id = db.Column(db.String, primary_key=True)
    dir_name = db.Column(db.String)
    patient_id = db.Column(db.String)
    accession_number = db.Column(db.String)
    series_number = db.Column(db.String)
    command = db.Column(db.String)
    running_time = db.Column(db.Time)
    status = db.Column(db.String)
    exception = db.Column(db.String)
    creation_time = db.Column(db.DateTime, default=datetime.now())
    started = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
    flag_finished = db.Column(db.Boolean, index=True)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return (
            '<TaskInfo ' +
            ', '.join(
                ['{0!r}: {1!r}'.format(*x) for x in self.__dict__.items()]) +
            '>'
        )


class TaskResult(db.Model):
    __tablename__ = 'celery_taskmeta'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(155))
    status = db.Column(db.String(50))
    result = db.Column(db.Binary)
    date_done = db.Column(db.TIMESTAMP)
    traceback = db.Column(db.String)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return (
            '<TaskInfo ' +
            ', '.join(
                ['{0!r}: {1!r}'.format(*x) for x in self.__dict__.items()]) +
            '>'
        )

db.create_all()
db.session.commit()


@celery_app.task
def download_task(command):
    # TODO: obsolete - dbc.store_task_start_time(download_task.request.id)

    task_info = TaskInfo.query.get(download_task.request.id)
    task_info.started = datetime.now()
    db.session.commit()

    print("++++++++++ task stored: " + download_task.request.id)

    args = shlex.split(command)
    app.logger.debug('Running args %s', args)


    # TODO: Delete this
    print('++++ DEBUG: STARTING TASK')

    output = subprocess.run(args, stderr=subprocess.PIPE, shell=False)
    time.sleep(3)

    # TODO: Delete this
    print('+++ DEBUG: FINISHED TASK')

    return download_task.request.id


@task_postrun.connect
def post_run(*args, **kwargs):
    task_id = kwargs['task_id']

    print('++++ POSTRUN FOR TASK_ID: ' + task_id)

    task_result = TaskResult.query.filter(TaskResult.task_id == task_id).first()
    task_info = TaskInfo.query.get(task_id)

    task_info.finished = datetime.now()
    task_info.flag_finished = True
    task_info.status = task_result.status

    print('++++ post run status ', task_info.status)

    if task_info.started:
        task_info.running_time = task_info.finished - task_info.started

    task_info.exception = task_result.traceback

    db.session.commit()


def store_task_info(task_id, dir_name, entry, command):
    task_info = TaskInfo(
        id=task_id,
        dir_name=dir_name,
        patient_id=entry['patient_id'],
        accession_number=entry['accession_number'],
        series_number=entry['series_number'],
        command=command,
        running_time=None,
        status='SUBMITTING',
        exception=None,
        started=None,
        finished=None,
        flag_finished=False
    )
    db.session.add(task_info)
    db.session.commit()


@app.route('/download', methods=['POST'])
def download():
    """ Ajax post to download series of images. """
    app.logger.info("download called")
    data = request.get_json(force=True)
    # list of objects with following keys
    #   -patient_id
    #   -study_id
    #   -series_id
    #   -accession_number
    #   -series_number
    # For more details see script.js
    series_list = data.get('data', '')
    dir_name = data.get('dir', '')

    for entry in series_list:
        download_command = construct_download_command(
            DCMTK_CONFIG,
            PACS_CONFIG,
            entry,
            OUTPUT_DIR,
            dir_name
        )

        # TODO: Obsolete - result = download_task.delay(download_command)
        result = download_task.delay(download_command)
        # result = download_task.apply_async([download_command],
        #                                    link=success_handler.s(),
        #                                    link_error=error_handler.s())

        store_task_info(result.id, dir_name, entry, download_command)

        # TODO: obsolete - dbc.store_task_registered_time(result.id)

    return json.dumps({'status': 'OK', 'series_length': len(series_list)})


@app.route('/flush')
def flush():
    # TODO: Need to implement FLUSH
    TaskInfo.query.delete()
    db.session.commit()

    return 'Queue cleared'


@app.route('/')
def main():
    """ Renders the initial page. """
    return render_template('search.html',
                           version=VERSION,
                           page=0,
                           offset=0,
                           params={'query': '*:*'})


@app.route('/transfer', methods=['POST'])
def transfer():
    """ Ajax post to transfer series of images to <target> PACS node. """
    data = request.get_json(force=True)
    target = data.get('target', '')
    series_list = data.get('data', '')
    app.logger.info("transfer called and sending to %s", target)

    # TODO: Swap this
    study_size = transfer_series(series_list, target)

    return str(study_size)


@app.route('/transfers')
def transfers():
    """ Renders the status of the transfers. """
    return render_template('transfers.html', version=VERSION)


@app.route('/transfers/data')
def transfersdata():
    data = transfer_status()
    return render_template('partials/transfers-status.html', tasks=data)


@app.route('/tasks')
def tasks():
    """ Renders a status page on the current tasks. A tasks is either
    to download or to transfer series.
    """
    return render_template('tasks.html', version=VERSION)


def download_status():
    """ Returns all done tasks and open tasks as lists.
    A task is a named tuple.
    """

    finished_task_ids = set(db.session.query(TaskResult.task_id).all())
    unfinished_task_ids = set(db.session.query(TaskInfo.id).filter(~TaskInfo.flag_finished))

    print('+++count unfinished ', len(unfinished_task_ids))
    print('+++count results ', len(finished_task_ids))

    misaligned_ids = unfinished_task_ids.intersection(finished_task_ids)
    print('+++count misaligned ', len(misaligned_ids))

    for misaligned_id in misaligned_ids:
        task_info = TaskInfo.query.filter(TaskInfo.id == misaligned_id).first()
        task_result = TaskResult.query.filter(TaskResult.task_id == misaligned_id).first()
        task_info.status = task_result.status
        task_info.flag_finished = True

    print(unfinished_task_ids)

    db.session.commit()

    unfinished_tasks = TaskInfo.query.filter(~TaskInfo.flag_finished).all()
    finished_tasks = TaskInfo.query.filter(TaskInfo.flag_finished).all()

    print(' +++ Unfinished len: ', len(unfinished_tasks))

    return unfinished_tasks, finished_tasks


@app.route('/tasks/data')
def tasksdata():
    print('+++++++ GETTING RUNNING TASKS')
    data = download_status()
    return render_template('partials/tasks-status.html', tasks=data)


@app.route('/terms')
def terms():
    """ Renders a page about term information. Only internal use. """
    data = get_terms_data(app.config)
    return render_template('terms.html', terms=data)


@app.route('/search', methods=['POST', 'GET'])
def search():
    """ Renders the search results. """
    params = request.form
    payload = query_body(params, RESULT_LIMIT)
    headers = {'content-type': "application/json"}
    try:
        response = get(solr_url(app.config), data=json.dumps(payload), headers=headers)
    except RequestException:
        return render_template('search.html',
                               params={},
                               error='No response from Solr, is it running?',
                               trace=solr_url(app.config))

    if response.status_code >= 400:
        return render_template('search.html',
                               params={},
                               page=0,
                               error=response.reason,
                               trace=response.url)
    elif response.status_code >= 500:
        result = response.json()
        error = result['error']
        msg = result['error']['msg']
        trace = error.get('trace', '')
        return render_template('search.html',
                               params={},
                               page=0,
                               offset=0,
                               error='Solr failed: ' + msg,
                               trace=trace)
    else:
        app.logger.debug('Calling Solr with url %s', response.url)
        app.logger.debug('Request body %s', json.dumps(payload))
        data = response.json()
        docs = data['grouped']['PatientID']
        docs = group(docs)
        facets = prepare_facets(data.get('facets', []), request.url)
        results = data['grouped']['PatientID']['ngroups']
        page = params.get('page', 0)
        offset = params.get('offset', 0)
        paging = calc(results, page, RESULT_LIMIT)
        demo = DEMO
        return render_template('result.html',
                               docs=docs,
                               results=results,
                               facets=facets,
                               payload=payload,
                               facet_url=request.url,
                               params=params,
                               paging=paging,
                               version=VERSION,
                               report_show_url=REPORT_SHOW_URL,
                               modalities=params.getlist('Modality'),
                               page=page,
                               offset=0,
                               demo=demo)
