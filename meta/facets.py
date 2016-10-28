from meta.query_param import set_query_parameter


def prepare_facets(facets, url):
    if not facets:
        return []
    else:
        for key, value in facets.items():
            if type(value) is dict:
                for bucket_key, bucket_value in value.items():
                    for e in bucket_value:
                        value = '"{0}"'.format(e['val'])
                        new_url, clear = set_query_parameter(url, key, value)
                        e['url'] = new_url
                        e['clear'] = clear

    return facets
