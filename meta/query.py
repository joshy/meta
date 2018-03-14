import logging
from datetime import datetime

DEFAULT_PAYLOAD = {'offset': 0, 'limit': 1,
                   'params': {'group': 'true', 'group.field': 'PatientID',
                              'group.limit': 100, 'group.ngroups': 'true'}
                  }


def query_body(args, limit=100):
    body = DEFAULT_PAYLOAD.copy()
    body['limit'] = limit
    filters = []
    if args.get('SeriesDescription'):
        user_input = args.get('SeriesDescription').split(' ')
        series_descriptions = [x for x in user_input if x]
        logging.debug(series_descriptions)
        # A block join query, search all parents which have a child with
        # the specific series description, can be multiple
        filters = [
            '{!parent which=Category:parent}(+SeriesDescription:%s)' % x
            for x in series_descriptions
        ]

    body['query'] = 'RisReport:({})'.format(args.get('RisReport', '*'))

    if args.get('SeriesDescriptionFilter'):
        body['params']['fl'] = '*,[child parentFilter=Category:parent childFilter="SeriesDescription:{}" limit=200]'.format(args.get('SeriesDescriptionFilter'))
    else:
        body['params']['fl'] = '*,[child parentFilter=Category:parent limit=200]'

    body['offset'] = int(args.get('offset', '0'))
    body['filter'] = _create_filter_query(args) + filters

    return body


def _create_filter_query(args):
    result = [_filter('StudyDescription', args),
              _filter('PatientID', args),
              _filter('PatientName', args),
              _filter('AccessionNumber', args),
              _filter_list('Modality', args),
              _create_date_range(args.get('StartDate'), args.get('EndDate'))]
    return [x for x in result if x is not None]


def _filter(element, args):
    if args.get(element):
        return element + ':(' + args.get(element) + ')'


def _filter_list(element, args):
    if args.getlist(element):
        a_list = args.getlist(element)
        joined = ' OR '.join(a_list)
        return element + ':(' + joined + ')'


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
