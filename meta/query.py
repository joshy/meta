import datetime


default_payload = {'start': 0, 'rows': 500, 'wt': 'json', 'q': '*:*', 'facet': 'true', 
    'json.facet': '{ SeriesDescription:{type:terms, field:SeriesDescription}, StudyDescription:{type:terms, field:StudyDescription}}'}



def create_payload(search_term, start_date, end_date):
    payload = _add_search_term(search_term)
    return _add_date_range(start_date, end_date, payload)


def _add_search_term(search_term):
    print(default_payload)
    default_payload['q'] = search_term
    return default_payload
    

def _add_date_range(start_date, end_date, payload):
    if (not start_date) and (not end_date):
        return payload

    start_date = _date_to_long(start_date)
    end_date = _date_to_long(end_date)
    start_date = start_date if start_date else '*'
    end_date = end_date if end_date else '*'
    print(payload['q'])
    if (payload['q']):
        payload['q'] = payload['q'] + ' AND '
    payload['q'] = payload['q'] + 'StudyDate:[' + start_date + ' TO ' + end_date + ']'
    print(payload)
    return payload


def _date_to_long(date):
    """
    Converts a date from the frontend which is passed in the following format
    31.12.2016 to 20161231. This is how it is stored in the metadata db.
    """
    return datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y%m%d') if date else ''
