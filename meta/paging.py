import meta.settings
import meta.query_param


def calc(results, url, current):
    print(current)
    limit = meta.settings.RESULT_LIMIT
    pages = results // limit
    r = []
    current_page = max(int(current) // limit, 1)

    for x in range(1, min(pages + 1, 21)):
        new_url = meta.query_param.set_query_parameter(url, 'offset', x * limit)
        r.append((x, new_url, True if x == current_page else False))
    return r
