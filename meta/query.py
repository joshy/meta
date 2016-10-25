import logging
import json
from datetime import datetime

default_payload = {'offset': 0, 'limit': 500, 'query': '*:*',
                   'facet':
                       {'SeriesDescription':
                        {'type': 'terms', 'field': 'SeriesDescription'},
                        'StudyDescription':
                            {'type': 'terms', 'field': 'StudyDescription'}
                        }
                   }


def json_body(args):
    body = default_payload
    body['query'] = args.get('q', '*')
    body['offset'] = args.get('offset', '0')

    date_range = _create_date_range(args.get('StartDate'), args.get('EndDate'))
    if not date_range:
        body['query'] = body['query'] + ' AND ' + date_range
    r = json.dumps(body)
    print(r)
    return r, body


def _create_filter_query(args):
    result = []
    if args.get('StudyDescription'):
        result.append('StudyDescription:"' + args.get('StudyDescription') + "'")
    return result


def _create_date_range(start_date, end_date):
    if not (start_date or end_date):
        return None
    _start_date = _convert(start_date)
    _end_date = _convert(end_date)

    return 'StudyDate:[' + _start_date + ' TO ' + _end_date + ']'


def _convert(date):
    """
    Converts a date from the frontend which is passed in the following format
    31.12.2016 to 20161231. This is how it is stored in solr.
    """
    try:
        return datetime.strptime(date, '%d.%m.%Y').strftime('%Y%m%d')
    except ValueError:
        logging.warning('Could not parse date %s, setting it to "*"', date)
        return '*'
