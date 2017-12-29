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

from meta.redis_controller import download_status, flush
from meta.pull import transfer_series, transfer_status

from celery import Celery
from celery.signals import task_success, task_failure

import shlex
import subprocess

import meta.command as command

import meta.redis_controller as rc


def create_celery_qm(flask_app):
    celery_qm = Celery(
        flask_app.import_name,
        broker=flask_app.config['CELERY_BROKER_URL']
    )

    celery_qm.conf.update(flask_app.config)
    TaskBase = celery_qm.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery_qm.Task = ContextTask
    return celery_qm


celery = create_celery_qm(app)


@celery.task
def download_task(command):
    rc.store_task_start_time(download_task.request.id)

    args = shlex.split(command)
    app.logger.debug('Running args %s', args)

    output = subprocess.run(args, stderr=subprocess.PIPE, shell=False)


@task_success.connect
def task_success(**keywords):
    rc.change_task_status(
        download_task.request.id,
        'SUCCESS'
    )


@task_failure.connect
def task_failure(**keywords):
    error_template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    error_type = type(keywords['exception']).__name__
    error_arguments = keywords['exception']
    error_message = error_template.format(error_type, error_arguments)

    rc.change_task_status(
        keywords['task_id'],  # download_task.request.id,
        'FAILED',
        error_message
    )


@app.route('/')
def main():
    """ Renders the initial page. """
    return render_template('search.html',
                           version=VERSION,
                           page=0,
                           offset=0,
                           params={'query': '*:*'})


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


@app.route('/flush')
def flush():
    rc.flush()
    return 'Queue cleared'


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
        download_command = command.construct_command(
            DCMTK_CONFIG,
            PACS_CONFIG,
            entry,
            OUTPUT_DIR,
            dir_name
        )

        result = download_task.delay(download_command)

        rc.store_task_info(result.id, dir_name, entry, download_command)
        rc.store_task_registered_time(result.id)

    return json.dumps({'status':'OK', 'series_length': len(series_list)})


@app.route('/transfer', methods=['POST'])
def transfer():
    """ Ajax post to transfer series of images to <target> PACS node. """
    data = request.get_json(force=True)
    target = data.get('target', '')
    series_list = data.get('data', '')
    app.logger.info("transfer called and sending to %s", target)
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


@app.route('/tasks/data')
def tasksdata():
    data = download_status()
    return render_template('partials/tasks-status.html', tasks=data)


@app.route('/terms')
def terms():
    """ Renders a page about term information. Only internal use. """
    data = get_terms_data(app.config)
    return render_template('terms.html', terms=data)


