import json

from requests import get, RequestException
from flask import render_template, request, current_app, Blueprint

from meta.query import query_body
from meta.paging import calc
from meta.grouping import group
from meta.solr import solr_url
from meta.terms import get_terms_data

from meta.command_creator import construct_download_command
from meta.command_creator import construct_transfer_command

from meta.config import dcmtk_config, pacs_config

from meta.queue_manager import submit_task, task_status, flush_db

DOWNLOAD = 'download'
TRANSFER = 'transfer'

pacs_crawler_blueprint = Blueprint('pacs_crawler_page',
                                   __name__,
                                   template_folder='templates')


@pacs_crawler_blueprint.route('/')
def main():
    """ Renders the initial page. """
    return render_template('search.html',
                           version=current_app.config['VERSION'],
                           page=0,
                           offset=0,
                           params={'query': '*'})


def _transfer_series(series_list, target):
    """ Transfer the series to target PACS node. """
    study_id_list = [entry['study_id'] for entry in series_list]
    study_id_set = set(study_id_list)
    current_app.logger.debug('Transferring ids: %s', study_id_set)

    for study_id in study_id_set:
        transfer_command = construct_transfer_command(
            dcmtk_config(current_app.config),
            pacs_config(current_app.config),
            target,
            study_id
        )
        entry = {'study_id': study_id, 'task_type': 'transfer'}
        submit_task(None, entry, transfer_command)

    return len(study_id_set)


@pacs_crawler_blueprint.route('/download', methods=['POST'])
def download():
    """ Ajax post to download series of images. """
    current_app.logger.info("download called")
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
            dcmtk_config(current_app.config),
            pacs_config(current_app.config),
            entry,
            current_app.config['IMAGE_FOLDER'],
            dir_name
        )
        entry['task_type'] = 'download'
        submit_task(dir_name, entry, download_command)

    return json.dumps({'status': 'OK', 'series_length': len(series_list)})


@pacs_crawler_blueprint.route('/transfer', methods=['POST'])
def transfer():
    """ Ajax post to transfer series of images to <target> PACS node. """
    data = request.get_json(force=True)
    target = data.get('target', '')
    series_list = data.get('data', '')
    current_app.logger.info("transfer called and sending to %s", target)

    study_size = _transfer_series(series_list, target)

    return str(study_size)


@pacs_crawler_blueprint.route('/transfers')
def transfers():
    """ Renders the status of the transfers. """
    return render_template('transfers.html', version=current_app.config['VERSION'])


@pacs_crawler_blueprint.route('/transfers/data')
def transfersdata():
    data = task_status(TRANSFER)
    return render_template('partials/transfers-status.html', tasks=data)


@pacs_crawler_blueprint.route('/tasks/data')
def tasksdata():
    data = task_status(DOWNLOAD)
    return render_template('partials/tasks-status.html', tasks=data)


@pacs_crawler_blueprint.route('/tasks')
def tasks():
    """ Renders a status page on the current tasks. A tasks is either
    to download or to transfer series.
    """
    return render_template('tasks.html', version=current_app.config['VERSION'])


@pacs_crawler_blueprint.route('/flush')
def flush():
    flush_db()
    return 'Queue cleared'


@pacs_crawler_blueprint.route('/terms')
def terms():
    """ Renders a page about term information. Only internal use. """
    data = get_terms_data(current_app.config)
    return render_template('terms.html', terms=data)


@pacs_crawler_blueprint.route('/search', methods=['POST', 'GET'])
def search():
    """ Renders the search results. """
    params = request.form
    payload = query_body(params, current_app.config['RESULT_LIMIT'])
    headers = {'content-type': "application/json"}
    try:
        response = get(
            solr_url(current_app.config),
            data=json.dumps(payload),
            headers=headers
        )
    except RequestException:
        return render_template('search.html',
                               params={},
                               error='No response from Solr, is it running?',
                               trace=solr_url(current_app.config))

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
        current_app.logger.debug('Calling Solr with url %s', response.url)
        current_app.logger.debug('Request body %s', json.dumps(payload))
        data = response.json()
        docs = data['grouped']['PatientID']
        docs = group(docs)
        #facets = prepare_facets(data.get('facets', []), request.url)
        results = data['grouped']['PatientID']['ngroups']
        page = params.get('page', 0)
        offset = params.get('offset', 0)
        paging = calc(results, page, current_app.config['RESULT_LIMIT'])
        demo = current_app.config['DEMO']
        return render_template('result.html',
                               docs=docs,
                               results=results,
                               #facets=facets,
                               payload=payload,
                               facet_url=request.url,
                               params=params,
                               paging=paging,
                               version=current_app.config['VERSION'],
                               report_show_url=current_app.config['REPORT_SHOW_URL'],
                               modalities=params.getlist('Modality'),
                               page=page,
                               offset=0,
                               demo=demo)
