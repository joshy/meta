from itertools import groupby


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

    return groups
