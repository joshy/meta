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

