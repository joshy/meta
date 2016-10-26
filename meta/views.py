import requests
import json

from flask import render_template, request

import meta.query
from meta import app
from meta.pull import *
from meta.paging import calc


@app.route('/')
def main():
    return render_template('search.html', params={'query': '*'})


@app.route('/bulksearch')
def bulk_search():
    return render_template('bulk-search.html')


@app.route('/search')
def search():
    params = request.args
    print(params.getlist('Modality'))

    study_desc, series_desc = get_params(params)
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
        docs = data['response']['docs']
        facets = data.get('facets', [])
        results = data['response']['numFound']
        disable_links = (True if study_desc or series_desc else False)
        return render_template('table.html', docs=docs, results=results,
                               facets=facets,
                               payload=payload,
                               facet_url=request.url,
                               disable_links=disable_links,
                               params=params,
                               paging=calc(results, request.url, params.get('offset', '1')),
                               modalities=params.getlist('Modality'))
    except json.JSONDecodeError:
        return render_template('search.html', error='Can\'t decode JSON, is '
                                                    'Solr running?')


@app.route('/download', methods=['POST'])
def download():
    series_list = request.get_json(force=True)
    meta.pull.download(series_list)
    return 'OK'


@app.route('/transfer/<target>', methods=['POST'])
def transfer(target):
    app.logger.debug("transfer called and sending to %s", target)
    series_list = request.get_json(force=True)
    meta.pull.transfer(series_list, target)
    return 'OK'


def get_params(args):
    return args.get('StudyDescription'), \
           args.get('SeriesDescription')
