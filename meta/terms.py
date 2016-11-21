import logging
import requests

from datetime import datetime
from meta.solr import solr_terms_url


def get_data():
    params = [('terms.fl', 'StudyDescription'),
              ('terms.fl', 'SeriesDescription'),
              ('terms.fl', 'InstitutionName'),
              ('terms.limit', 1000),
              ('wt', 'json')]

    response = requests.get(solr_terms_url(), params=params)
    return response.json()
