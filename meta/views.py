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

import shlex
import subprocess

from meta.command_creator import construct_download_command
from meta.command_creator import construct_transfer_command

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from concurrent.futures import ThreadPoolExecutor

import sys

import time
from meta.queue_manager import TaskInfo, submit_task, task_status

from meta.queue_manager_models import db

DOWNLOAD_TYPE = 'download'
TRANSFER_TYPE = 'transfer'


#
# class TaskInfo(db.Model):
#     __tablename__ = 'task_info'
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     dir_name = db.Column(db.String)
#     patient_id = db.Column(db.String)
#     accession_number = db.Column(db.String)
#     series_number = db.Column(db.String)
#
#     study_id = db.Column(db.String)  # study_id
#
#     creation_time = db.Column(db.DateTime, default=datetime.now())
#     execution_time = db.Column(db.DateTime, default=datetime.now())  # execution_time # TODO: Not sure if this is used
#     started = db.Column(db.DateTime)
#     finished = db.Column(db.DateTime)
#     running_time = db.Column(db.Time)
#     flag_finished = db.Column(db.Boolean, index=True)
#     exception = db.Column(db.String)
#     command = db.Column(db.String)
#     status = db.Column(db.String)
#     type = db.Column(db.String, index=True)
#
#     def __len__(self):
#         return len(self.__dict__)
#
#     def __repr__(self):
#         return (
#             '<TaskInfo ' +
#             ', '.join(
#                 ['{0!r}: {1!r}'.format(*x) for x in self.__dict__.items()]) +
#             '>'
#         )



#
# def store_task_info(dir_name, entry, command):
#     # TODO: If there was no Flask related inheritance, we could use in-db inheritance
#     task_info = TaskInfo(
#         dir_name=dir_name,
#         study_id=entry.get('study_id'),
#         patient_id=entry.get('patient_id'),
#         accession_number=entry.get('accession_number'),
#         series_number=entry.get('series_number'),
#         command=command,
#         running_time=None,
#         status='REGISTERED',
#         exception=None,
#         started=None,
#         finished=None,
#         flag_finished=False,
#         type=entry['type']
#     )
#     db.session.add(task_info)
#     db.session.commit()
#
#     return task_info.id


# def _bash_task(task_id, args):
#     task_info = TaskInfo.query.get(task_id)
#     task_info.started = datetime.now()
#     task_info.status = 'SUBMITTED'
#     db.session.commit()
#
#     try:
#         # TODO: UNCOMMENT THIS FOR PRODUCTION!
#         #output = subprocess.run(args, stderr=subprocess.PIPE, shell=False)
#         time.sleep(5)
#         raise ValueError
#
#         task_info.status = 'SUCCEEDED'
#         print('+++ SUCCESS', task_id)
#     except:
#         task_info.status = 'FAILED'
#         task_info.exception = '{}{}{}'.format(*sys.exc_info())
#         print('+++ FAIL', task_id)
#     finally:
#         print('+++ FLAGGED FINISHED')
#         task_info.flag_finished = True
#         task_info.finished = datetime.now()
#         if task_info.started:
#             task_info.running_time = task_info.finished - task_info.started
#         db.session.commit()
#
#     # TODO: Delete this
#     print('+++ FINISHED', task_id)
#
#     return output


# def submit_task(app_db, dir_name, entry, command):
#     task_id = store_task_info(dir_name, entry, command)
#     print("++++ QUEUE TASK", task_id)
#
#     args = shlex.split(command)
#     app.logger.debug('Running args %s', args)
#
#     print('++++ SUBMITTING TASK', task_id)
#     task_info = TaskInfo.query.get(task_id)
#     task_info.status = 'SUBMITTING'
#     app_db.session.commit()
#
#     executor.submit(_bash_task, task_id, args)
#
#     return task_id


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
        entry['type'] = 'download'

        submit_task(dir_name, entry, download_command)

    return json.dumps({'status': 'OK', 'series_length': len(series_list)})


@app.route('/flush')
def flush():
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


def transfer_series(series_list, target):
    """ Transfer the series to target PACS node. """
    study_id_list = [entry['study_id'] for entry in series_list]
    study_id_set = set(study_id_list)
    app.logger.debug('Transferring ids: %s', study_id_set)

    for study_id in study_id_set:
        transfer_command = construct_transfer_command(
            DCMTK_CONFIG,
            PACS_CONFIG,
            target,
            study_id
        )
        entry = {'study_id': study_id, 'type': 'transfer'}
        submit_task(None, entry, transfer_command)

    return len(study_id_set)


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
    data = task_status(TRANSFER_TYPE)
    return render_template('partials/transfers-status.html', tasks=data)


@app.route('/tasks/data')
def tasksdata():
    print('+++++++ GETTING RUNNING TASKS')
    data = task_status(DOWNLOAD_TYPE)
    return render_template('partials/tasks-status.html', tasks=data)


@app.route('/tasks')
def tasks():
    """ Renders a status page on the current tasks. A tasks is either
    to download or to transfer series.
    """
    return render_template('tasks.html', version=VERSION)


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
