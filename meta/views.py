import json
from requests import get, RequestException
from flask import render_template, request, redirect, url_for

from meta.app import app, VERSION, DEMO, RESULT_LIMIT
from meta.query import query_body
from meta.paging import calc
from meta.pull import download_series, transfer_series, status
from meta.facets import prepare_facets
from meta.grouping import group
from meta.solr import solr_url
from meta.terms import get_terms_data


@app.route('/')
def main():
    """ Renders the initial page. """
    return render_template('search.html',
                           version=VERSION,
                           params={'query': '*:*'})


@app.route('/search')
def search():
    """ Renders the search results. """
    params = request.args
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
                                   error='Solr failed: ' + msg,
                                   trace=trace)

        app.logger.debug('Calling Solr with url %s', response.url)
        app.logger.debug('Request body %s', json.dumps(payload))
        data = response.json()
        docs = data['grouped']['PatientID']
        docs = group(docs)
        facets = prepare_facets(data.get('facets', []), request.url)
        results = data['grouped']['PatientID']['ngroups']
        paging = calc(results, request.url, params.get('offset', '1'), RESULT_LIMIT)
        demo = app.config['DEMO']
        return render_template('result.html',
                               docs=docs,
                               results=results,
                               facets=facets,
                               payload=payload,
                               facet_url=request.url,
                               params=params,
                               paging=paging,
                               version=app.config['VERSION'],
                               modalities=params.getlist('Modality'),
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


@app.route('/transfer/<target>', methods=['POST'])
def transfer(target):
    """ Ajax post to transfer series of images to <target> PACS node. """
    app.logger.info("transfer called and sending to %s", target)
    series_list = request.get_json(force=True)
    transfer_series(series_list, target)
    return 'OK'


@app.route('/tasks')
def tasks():
    """ Renders a status page on the current tasks. A tasks is either
    to download or to transfer series.
    """
    return render_template('tasks.html', version=app.config['VERSION'])


@app.route('/tasks/data')
def tasksdata():
    data = status()
    return render_template('partials/tasks-status.html', tasks=data)


@app.route('/terms')
def terms():
    """ Renders a page about term information. Only internal use. """
    data = get_terms_data()
    return render_template('terms.html', terms=data)
