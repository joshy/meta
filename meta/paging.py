import meta.settings
from meta.query_param import set_query_parameter

PAGING_LINKS = 20


def calc(results, url, current):
    limit = meta.settings.RESULT_LIMIT
    pages = results // limit
    if results % limit > 0:
        pages += 1

    r = []
    current_page = max(int(current) // limit, 0)
    min_page = max(current_page - (PAGING_LINKS // 2), 0)
    max_page = min(min_page + PAGING_LINKS, pages)

    for x in range(min_page, max_page):
        new_url, _ = set_query_parameter(url, 'offset', x * limit)
        r.append((x + 1,
                  new_url,
                  # highlight current page marker
                  True if x == current_page else False,
                  # replace first page number with arrow
                  True if min_page >= 1 else False))
    if len(r) == 1:
        return []
    print(r)
    return r
