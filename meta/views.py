import requests
import urllib.parse
from meta import app
from flask import render_template, request

import meta.query
from meta.settings import *


@app.route('/')
def main():
    return render_template('search.html')


@app.route('/search')
def search():
    search_term, start_date, end_date, facet_key, facet_value = search_params(request)
    payload = meta.query.create_payload(search_term, start_date, end_date, facet_key, facet_value)
    r = requests.get(SOLR_URL, params=payload)
    print(r.url)
    data = r.json()
    docs = data['response']['docs']
    facets = data['facets']
    results = data['response']['numFound']
    params = data['responseHeader']['params']
    return render_template('table.html', docs=docs, results=results, facets=facets, searchterm=search_term, 
        startdate=start_date, enddate=end_date, payload=payload, facet_url=request.url)


@app.route('/download', methods=['POST'])
def download():
    data = request.get_json(force=True)
    print(data)
    return 'OK'

def search_params(request):
    return request.args.get('q'), request.args.get('StartDate'), request.args.get('EndDate'), request.args.get('FacetKey'), request.args.get('FacetValue')
