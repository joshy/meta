from meta.query_param import set_query_parameter

# Total number of paging links to render left and
# right to the current page. Is capped at 0 and
# last page.
PAGING_LINKS = 5


def calc(results, current, limit=100):
    # type (Int, String, Int) -> (Int, bool, bool)
    """
    Zero based pagging. PAGING_LINKS is the number of
    pages links to be shown. Because results can be easily
    more than e.g. 50 pages, then only number of PAGING_LINKS are
    rendered.
    """

    # total number of pages, limit is number of result per page
    pages = results // limit
    if results % limit > 0:
        pages += 1

    result = []
    current_page = int(current)
    min_page = max(current_page - PAGING_LINKS + 1, 0)
    max_page = min(current_page + PAGING_LINKS, pages)

    for page in range(min_page, max_page):
        result.append((page,
                       # highlight current page marker
                       True if page == current_page else False,
                       # replace first page number with arrow
                       True if min_page >= 1 else False,
                       True if current_page >= pages - PAGING_LINKS else False))
    if len(result) == 1:
        return []
    return result
