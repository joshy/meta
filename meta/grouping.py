from itertools import groupby
from datetime import datetime


def group(groups):
    """
    Groups all the documents according to the AccessionNumber. This is done
        as a post processing step, because Solr doesn't support sub grouping.
    """
    for g in groups['groups']:
        grouped = {}
        for key, value in groupby(g['doclist']['docs'],
                                  lambda x: x.get('AccessionNumber', '')):
            grouped[key] = list(value)
            g['by_AccessionNumber'] = grouped
            patient = {}
            first_entry = list(grouped.values())[0][0]
            patient['name'] = first_entry.get('PatientName', None)
            birthdate = first_entry.get('PatientBirthDate', None)
            if birthdate is not None:
                patient['birthdate'] = datetime.strptime(
                    str(birthdate), '%Y%m%d').strftime('%d.%m.%Y')
            g['patient'] = patient

    return groups
