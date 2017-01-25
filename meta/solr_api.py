"""
This API is indendet to be used for external applications, like jupyter
notebooks.
"""

import pandas as pd
import json

from itertools import chain
from requests import get

from meta.app import app
from meta.solr import solr_url
from meta.grouping import group

import meta.query as q
import werkzeug.datastructures as w

INTERNAL_LIMIT = 100

def search_solr(params):
    # Dict[str, [str | datetime]] -> pandas.DataFrame
    """
    Search the solr backend and returns all result. The paging through the
    result is done internal. So a query with '*:*' and no filters set could
    take some time. The following keys are taken into account:
      * query: str
      * StartDate: datetime
      * EndDate: datetime
      * StudyDescription: str
      * SeriesDescription: str
      * PatientID: str
      * PatientName: str (Exact name match would be "John\^Doe")
      * AccessionNumber: str
      * Modality: str
      * InstitutionName: str

    Returns a pandas dataframe.
    """

    results = _result(params)
    data_frames = []
    for page in range(0, results, INTERNAL_LIMIT):
        params['offset'] = str(page)
        data_frames.append(_call(params))
    return pd.concat(data_frames)


def _result(params):
    # MultiDict[str, str] -> json
    headers = {'content-type': "application/json"}
    payload = q.query_body(w.MultiDict(params), limit=INTERNAL_LIMIT)
    response = get(solr_url(app.config), data=json.dumps(payload), headers=headers)
    data = response.json()
    docs = data['grouped']['PatientID']
    results = int(docs['matches'])
    # add additional request to get the remaining results
    if results % INTERNAL_LIMIT > 0:
        results += INTERNAL_LIMIT
    return results


def _call(params):
    # MultiDict[str, str] -> json
    headers = {'content-type': "application/json"}
    payload = q.query_body(w.MultiDict(params), limit=INTERNAL_LIMIT)
    response = get(solr_url(app.config), data=json.dumps(payload), headers=headers)
    data = response.json()
    docs = data['grouped']['PatientID']
    docs = group(docs)

    result = list(chain(*chain(*[cgrp['by_AccessionNumber'].values()
                                 for cgrp in docs['groups']])))
    return pd.DataFrame(result)
