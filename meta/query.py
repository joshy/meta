import logging
from datetime import datetime

default_payload = {'start': 0, 'rows': 500, 'wt': 'json', 'q': '*:*',
                    #'sort': 'StudyDate asc',
                   'facet': 'true',

                   'json.facet':
                       '{ SeriesDescription: '
                       '{ type:terms, field:SeriesDescription}, '
                       'StudyDescription: '
                       '{ type:terms, field:StudyDescription}}'}


def create_payload(search_term, start_date, end_date, facet_key, facet_value):
    payload = _add_search_term(search_term)
    payload = _add_date_range(start_date, end_date, payload)
    return _add_facet_query(facet_key, facet_value, payload)


def _add_facet_query(facet_key, facet_value, payload):
    if facet_key and facet_value:
        payload['fq'] = facet_key + ':' + facet_value
    else:
        payload.pop('fq', None)
    return payload


def _add_search_term(search_term):
    default_payload['q'] = search_term
    return default_payload


def _add_date_range(start_date, end_date, payload):
    if not (start_date or end_date):
        return payload
    _start_date = _convert(start_date)
    _end_date = _convert(end_date)

    if payload["q"]:
        payload['q'] = payload['q'] + ' AND '
    payload['q'] = payload['q'] \
                   + 'StudyDate:[' + _start_date + ' TO ' + _end_date + ']'
    return payload


def _convert(date):
    """
    Converts a date from the frontend which is passed in the following format
    31.12.2016 to 20161231. This is how it is stored in the metadata db.
    """
    try:
        return datetime.strptime(date, '%d.%m.%Y').strftime('%Y%m%d')
    except ValueError:
        logging.warning('Could not parse date %s, setting it to "*"', date)
        return '*'
