import logging
import typing

import pandas as pd
from werkzeug.datastructures import MultiDict

from meta.client.api import SearchParams
from meta.query_all import query_all

##
# Example how to use the api to search for someting
# env PYTHONPATH=. python meta/client/example.py
##

params = SearchParams().start_date('01.01.2016').end_date(
    '31.12.2017').study_description('"schaedel"').build()
print(params)
result_df = query_all(params, 'http://meqpacscrllt01.uhbs.ch:8983/solr/ris_pacs_1/query')

for row in result_df.itertuples():
    acc = row.AccessionNumber
    report = row.RisReport
    with open('reports/' + acc + '.txt', 'w') as f:
        f.write(report)
