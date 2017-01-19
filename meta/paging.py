from meta.query_param import set_query_parameter

PAGING_LINKS = 20


def calc(results, current, limit=100):
    # type (Int, String, Int) -> (Int, bool, bool)

    # total number of pages, limit is number of result per page
    pages = results // limit
    if results % limit > 0:
        pages += 1

    result = []
    current_page = int(current)
    min_page = max(current_page - (PAGING_LINKS // 2), 0)
    max_page = min(min_page + PAGING_LINKS, pages)
    for page in range(min_page, max_page):
        result.append((page,
                       # highlight current page marker
                       True if page == (current_page) else False,
                       # replace first page number with arrow
                       True if min_page >= 1 else False))
    if len(result) == 1:
        return []
    return result
