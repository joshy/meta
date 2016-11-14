import requests
import json

from flask import render_template, request

import meta.query
from meta import app
from meta.pull import *
from meta.paging import calc
from meta.facets import prepare_facets
from meta.grouping import group
from meta.settings import SOLR_URL


@app.route('/')
def main():
    return render_template('search.html', params={'query': '*'})


@app.route('/search')
def search():
    params = request.args
    payload = meta.query.query_body(params)
    headers = {'content-type': "application/json"}
    r = requests.get(SOLR_URL, data=json.dumps(payload), headers=headers)
    app.logger.debug('Calling Solr with url %s', r.url)
    app.logger.debug('Request body %s', json.dumps(payload))
    try:
        if 400 == r.status_code or 500 == r.status_code:
            result = r.json()
            error = result['error']
            msg = result['error']['msg']
            trace = error.get('trace', '')

            return render_template('search.html',
                                   params={},
                                   error=' Call to Solr failed: ' + msg,
                                   trace=trace)
        data = r.json()
        docs = data['grouped']['PatientID']
        docs = group(docs)
        facets = prepare_facets(data.get('facets', []), request.url)
        results = data['grouped']['PatientID']['ngroups']
        paging = calc(results, request.url, params.get('offset', '1'))
        return render_template('result.html', docs=docs, results=results,
                               facets=facets,
                               payload=payload,
                               facet_url=request.url,
                               params=params,
                               paging=paging,
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
    meta.pull.download(series_list, dir_name)

    return 'OK'


@app.route('/transfer/<target>', methods=['POST'])
def transfer(target):
    app.logger.info("transfer called and sending to %s", target)
    series_list = request.get_json(force=True)
    meta.pull.transfer(series_list, target)

    return 'OK'
