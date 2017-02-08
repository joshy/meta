"""
This API is indendet to be used for external applications, like jupyter
notebooks.
"""
import json
from itertools import chain
from typing import Dict, Union

import pandas as pd
import werkzeug.datastructures as w
from requests import get

import meta.query as q
from meta.app import app
from meta.grouping import group
from meta.solr import solr_url

INTERNAL_LIMIT = 100

def search_solr(params, pages=None):
    # Dict[str, Union[str, datetime]], int -> pd.DataFrame
    """Search the solr backend and returns all result. The paging through the
    result is done internal. So a query with '*:*' and no filters set could
    take some time. The following keys are taken into account:
      * query: str
      * StartDate: datetime
      * EndDate: datetime
      * StudyDescription: str
      * SeriesDescription: str
      * PatientID: str
      * PatientName: str (Exact name match would be "John\\^Doe")
      * AccessionNumber: str
      * Modality: str
      * InstitutionName: str

    Returns a pandas dataframe.
    If no results are found it will return a empty DataFrame.
    If pages are passed, will return get that many paging results. This is not
    the *exact* number of results.
    """
    if not isinstance(params, dict):
        raise ValueError("params needs to be a dictionary, e.g. params={'query':'*:*'}")

    # check for solr query parse errors
    max_results, error_message = _result(params)
    if max_results < 0:
        raise ValueError(error_message)

    # if no results could be found return empty DataFrame
    if max_results == 0:
        return pd.DataFrame()

    if pages is None:
        pages = max_results
    else:
        pages = min(pages, max_results)

    data_frames = []
    for page in range(0, pages):
        params['offset'] = str(page)
        data_frames.append(_call(params))
    return pd.concat(data_frames)


def _result(params):
    # MultiDict[str, str] -> Tuple[int, str]
    """
    Makes a query and checks for number of results and if the query is valid.
    If the query contains an valid result, it returns a tuple
    (positive integer, None)
    If the query contains an error it returns this tuple
    (-1, <error message>)
    """
    headers = {'content-type': "application/json"}
    payload = q.query_body(w.MultiDict(params), limit=INTERNAL_LIMIT)
    response = get(solr_url(app.config), data=json.dumps(payload), headers=headers)
    data = response.json()
    error = data.get('error', None)

    if error is not None:
        msg = data['error']['msg']
        return -1, msg

    docs = data['grouped']['PatientID']
    results = int(docs['ngroups'])

    if results <= INTERNAL_LIMIT:
        return results, None
    else:
        results = int(docs['ngroups']) // INTERNAL_LIMIT
        if results % INTERNAL_LIMIT > 0:
            # add one additional request to get the remaining results
            results += 1
        return results, None


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
