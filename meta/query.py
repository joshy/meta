import logging
from datetime import datetime

import meta.settings

default_payload = {'offset': 0, 'limit': meta.settings.RESULT_LIMIT,
                   'query': '*:*',
                   'params': {'group': 'true', 'group.field': 'PatientID',
                              'group.limit': 10, 'group.ngroups': 'true'},
                   'facet':
                       {'SeriesDescription':
                        {'type': 'terms', 'field': 'SeriesDescription'},
                        'StudyDescription':
                            {'type': 'terms', 'field': 'StudyDescription'},
                        'Pivot':
                            {'type': 'terms', 'field': 'PatientID',
                             'limit': 100,
                             'facet': {
                                 'Studies': {
                                    'type': 'terms',
                                    'field': 'AccessionNumber'
                                    }
                                }
                             }
                        }
                   }


def query_body(args):
    body = default_payload.copy()
    body['query'] = args.get('query', '*')
    body['offset'] = args.get('offset', '0')

    date_range = _create_date_range(args.get('StartDate'), args.get('EndDate'))
    if date_range is not None:
        body['query'] = body['query'] + ' AND ' + date_range
    body['filter'] = _create_filter_query(args)

    return body


def _create_filter_query(args):
    result = [_filter('StudyDescription', args),
              _filter('SeriesDescription', args),
              _filter('PatientID', args),
              _filter('PatientName', args),
              _filter('AccessionNumber', args),
              _filter('Modality', args)]

    return [x for x in result if x is not None]


def _filter(element, args):
    if args.get(element):
        return '{0}:{1}'.format(element, args.get(element))


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
