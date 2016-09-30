from json import JSONDecodeError

import requests
from flask import render_template, request

import meta.query
from meta import app
from meta.pull import *


@app.route('/')
def main():
    return render_template('search.html')


@app.route('/search')
def search():
    search_term, start_date, end_date, study_desc, series_desc = get_params(request.args)
    payload = meta.query.create_payload(search_term, start_date, end_date,
                                        study_desc, series_desc)
    r = requests.get(SOLR_URL, params=payload)
    app.logger.debug('Calling Solr with url %s', r.url)
    try:
        data = r.json()
        docs = data['response']['docs']
        facets = data['facets']
        results = data['response']['numFound']
        return render_template('table.html', docs=docs, results=results,
                               facets=facets, searchterm=search_term,
                               startdate=start_date, enddate=end_date,
                               payload=payload, facet_url=request.url)
    except JSONDecodeError:
        return render_template('search.html', error='Can\'t decode JSON, is '
                                                    'Solr running?')


@app.route('/download', methods=['POST'])
def download():
    series_list = request.get_json(force=True)
    meta.pull.download(series_list)
    return 'OK'


@app.route('/transfer/<target>', methods=['POST'])
def transfer(target):
    app.logger.debug("tranfer called and sending to %s", target)
    series_list = request.get_json(force=True)
    meta.pull.transfer(series_list, target)
    return 'OK'


def get_params(args):
    return args.get('q'), args.get('StartDate'), \
           args.get('EndDate'), args.get('StudyDescription'), \
           args.get('SeriesDescription')
