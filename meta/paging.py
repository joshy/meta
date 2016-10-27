import meta.settings
from meta.query_param import set_query_parameter


def calc(results, url, current):
    limit = meta.settings.RESULT_LIMIT
    pages = results // limit
    if results % limit > 0:
        pages += 1

    r = []
    current_page = max(int(current) // limit, 0)

    for x in range(0, min(pages, 20)):
        new_url = set_query_parameter(url, 'offset', x * limit)
        r.append((x + 1, new_url, True if x == current_page else False))
    return r
