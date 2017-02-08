import json
from requests import get, RequestException
from flask import render_template, request
import sqlite3

from meta.app import app, VERSION, DEMO, RESULT_LIMIT
from meta.query import query_body
from meta.paging import calc
from meta.pull import download_series, transfer_series, download_status, transfer_status
from meta.facets import prepare_facets
from meta.grouping import group
from meta.solr import solr_url
from meta.terms import get_terms_data


@app.route('/')
def main():
    """ Renders the initial page. """
    return render_template('search.html',
                           version=VERSION,
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
        if response.status_code == 400 or response.status_code == 500:
            result = response.json()
            error = result['error']
            msg = result['error']['msg']
            trace = error.get('trace', '')
            return render_template('search.html',
                                   params={},
                                   offset='0',
                                   error='Solr failed: ' + msg,
                                   trace=trace)

        app.logger.debug('Calling Solr with url %s', response.url)
        app.logger.debug('Request body %s', json.dumps(payload))
        data = response.json()
        docs = data['grouped']['PatientID']
        docs = group(docs)
        facets = prepare_facets(data.get('facets', []), request.url)
        results = data['grouped']['PatientID']['ngroups']
        paging = calc(results, params.get('offset', '0'), RESULT_LIMIT)
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
                               modalities=params.getlist('Modality'),
                               offset=params.get('offset', '0'),
                               demo=demo)
    except RequestException:
        return render_template('search.html',
                               params={},
                               error='No response from Solr, is it running?')


@app.route('/download', methods=['POST'])
def download():
    """ Ajax post to download series of images. """
    app.logger.info("download called")
    data = request.get_json(force=True)
    # list of objects with following keys
    # "patient_id", "study_id", "series_id",
    # "accession_number", "series_number"
    # see script.js
    series_list = data.get('data', '')
    dir_name = data.get('dir', '')
    length = download_series(series_list, dir_name)
    return json.dumps({'status':'OK', 'series_length': length})


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
