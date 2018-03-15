import json
from math import ceil

import pandas as pd
from requests import RequestException, get
from werkzeug.datastructures import MultiDict

from meta.solr import solr_url
from meta.query import query_body, DEFAULT_PAYLOAD
from meta.app import app

class SearchParams(object):
    def __init__(self):
        self.args = MultiDict(DEFAULT_PAYLOAD)

    def patient_id(self, patient_id):
        self.args.add('PatientID', patient_id)
        return self

    def modality(self, modality):
        self.args.add('Modality', modality)
        return self

    def ris_report(self, keywords):
        self.args.add('query', keywords)
        return self

    def patient_name(self, patient_name):
        self.args.add('PatientName', patient_name)
        return self

    def accession_number(self, accession_number):
        self.args.add('AccessionNumber', accession_number)
        return self

    def study_description(self, study_description):
        self.args.add('StudyDescription', study_description)
        return self

    def series_dscription(self, series_description):
        self.args.add('SeriesDescription', series_description)
        return self

    def start_date(self, start_date: str):
        """ start_date format is dd.mm.yyyy """
        self.args.add('StartDate', start_date)
        return self

    def end_date(self, end_date: str):
        """ end_date format is dd.mm.yyyy """
        self.args.add('EndDate', end_date)
        return self

    def limit(self, limit):
        self.args.add('Limit', limit)
        return self

    def build(self):
        return self.args


def query_solr(search_params: MultiDict):
    limit = search_params.get('Limit', 100)
    query = query_body(search_params, limit=limit)
    query['params']['group'] = False
    query, docs, results_size = _query(query)
    requests_needed = ceil(results_size / limit)
    offsets = [x*limit for x in range(0, requests_needed)]
    result = []
    for i in offsets:
        query['offset'] = i
        _, docs, results_size = _query(query)
        result.append(pd.DataFrame.from_dict(docs))
    if result:
        return pd.concat(result)
    else:
        None


def _query(query):
    headers = {'content-type': "application/json"}
    try:
        response = get(
            solr_url(app.config), data=json.dumps(query), headers=headers)
        data = response.json()
        docs = data['response']['docs']
        results = data['response']['numFound']
        return query, docs, results
    except RequestException as e:
        print(e)
