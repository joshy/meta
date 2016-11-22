import requests
import json

from flask import render_template, request, redirect, url_for

import meta.query
from meta.app import app
from meta.pull import download_series, transfer_series
from meta.paging import calc
from meta.facets import prepare_facets
from meta.grouping import group
from meta.settings import solr_url


@app.route('/')
def main():
    return render_template('search.html', version=app.config['VERSION'],
                                          params={'query': '*:*'})


@app.route('/search')
def search():
    params = request.args
    payload = meta.query.query_body(params)
    headers = {'content-type': "application/json"}
    response = requests.get(solr_url(), data=json.dumps(payload), headers=headers)
    app.logger.debug('Calling Solr with url %s', response.url)
    app.logger.debug('Request body %s', json.dumps(payload))
    try:
        if 400 == response.status_code or 500 == response.status_code:
            result = response.json()
            error = result['error']
            msg = result['error']['msg']
            trace = error.get('trace', '')

            return render_template('search.html',
                                   params={},
                                   error=' Call to Solr failed: ' + msg,
                                   trace=trace)
        data = response.json()
        docs = data['grouped']['PatientID']
        docs = group(docs)
        facets = prepare_facets(data.get('facets', []), request.url)
        results = data['grouped']['PatientID']['ngroups']
        paging = calc(results, request.url, params.get('offset', '1'))
        return render_template('result.html',
                               docs=docs,
                               results=results,
                               facets=facets,
                               payload=payload,
                               facet_url=request.url,
                               params=params,
                               paging=paging,
                               version=app.config['VERSION'],
                               modalities=params.getlist('Modality'))
    except json.JSONDecodeError:
        return render_template('search.html',
                               params={},
                               error='Can\'t decode JSON, is Solr running?')


@app.route('/download', methods=['POST'])
def download():
    app.logger.info("download called")
    data = request.get_json(force=True)
    series_list = data.get('data', '')
    dir_name = data.get('dir', '')
    download_series(series_list, dir_name)

    return 'OK'


@app.route('/transfer/<target>', methods=['POST'])
def transfer(target):
    app.logger.info("transfer called and sending to %s", target)
    series_list = request.get_json(force=True)
    transfer_series(series_list, target)

    return 'OK'


@app.route('/settings')
def settings():
    app.logger.info("Settings called")
    return render_template('settings.html', core_name=app.config['CORE_NAME'])


@app.route('/settings', methods=['POST'])
def set_core():
    core_name = request.form['core_name']
    app.logger.info("Setting core to %s", core_name)
    app.config.update(CORE_NAME=core_name)
    return redirect(url_for('main'))
