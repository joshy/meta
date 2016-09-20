import requests
from meta import app
from flask import render_template, request

import meta.query


@app.route('/')
def main():
    return render_template('search.html')


@app.route('/search')
def search():
    search_term, start_date, end_date = search_params(request)
    payload = meta.query.create_payload(search_term, start_date, end_date)
    r = requests.get('http://localhost:8983/solr/pacs/query', params=payload)
    print(r.url)
    data = r.json()
    docs = data['response']['docs']
    facets= data['facets']
    results = data['response']['numFound']
    return render_template('table.html', docs=docs, results=results, facets=facets, searchterm=search_term, startdate=start_date,
                           enddate=end_date)


def search_params(request):
    return request.args.get('q'), request.args.get('StartDate'), request.args.get('EndDate')
