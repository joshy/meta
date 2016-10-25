import requests
import json

from flask import render_template, request

import meta.query
from meta import app
from meta.pull import *


@app.route('/')
def main():
    return render_template('search.html')


@app.route('/bulksearch')
def bulk_search():
    return render_template('bulk-search.html')


@app.route('/foo')
def foo():
    payload = {'query': 'lorem'}
    j = json.dumps(payload)
    print(j)
    headers = {'content-type': "application/json"}
    req = requests.Request('GET', SOLR_URL, data=j, headers=headers, params={'debug': 'true'})
    prepared = req.prepare()

    def pretty_print_POST(req):
        """
        At this point it is completely built and ready
        to be fired; it is "prepared".

        However pay attention at the formatting used in
        this function because it is programmed to be pretty
        printed and may differ from the actual request.
        """
        print('{}\n{}\n{}\n\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))

    pretty_print_POST(prepared)

    s = requests.Session()
    res = s.send(prepared)

    data = res.json()
    print(data)
    docs = data['response']['docs']
    facets = data.get('facets', [])
    results = data['response']['numFound']
    disable_links = True
    return render_template('table.html', docs=docs, results=results,
                           facets=facets, searchterm='',
                           startdate='', enddate='',
                           payload=payload, facet_url=request.url,
                           disable_links=disable_links)


@app.route('/search')
def search():
    search_term, start_date, end_date, study_desc, series_desc = get_params(request.args)
    payload = meta.query.json_body(request.args)
    headers = {'content-type': "application/json"}
    r = requests.get(SOLR_URL, data=payload, headers=headers)
    app.logger.debug('Calling Solr with url %s', r.url)
    try:
        if 400 == r.status_code or 500 == r.status_code:
            result = r.json()
            error = result['error']
            msg = result['error']['msg']
            trace = error.get('trace', '')

            return render_template('search.html',
                                   error=' Call to Solr failed: ' + msg,
                                   trace=trace)
        data = r.json()
        docs = data['response']['docs']
        facets = data.get('facets', [])
        results = data['response']['numFound']
        disable_links = (True if study_desc or series_desc else False)
        return render_template('table.html', docs=docs, results=results,
                               facets=facets, searchterm=search_term,
                               startdate=start_date, enddate=end_date,
                               payload=payload, facet_url=request.url,
                               disable_links=disable_links)
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
    return args.get('q'), args.get('StartDate'), \
           args.get('EndDate'), args.get('StudyDescription'), \
           args.get('SeriesDescription')
