import logging
import typing


import pandas as pd
from werkzeug.datastructures import MultiDict

from meta.client.api import SearchParams, query_solr


##
# Example how to use the api to search for someting
# env PYTHONPATH=. python meta/client/example.py
##



params = SearchParams().study_description("MRI Herz").start_date(
    '01.07.2016').end_date('31.01.2018').series_dscription(
        '*_KM_MOCO_T1').build()
result_df = query_solr(params)


writer = pd.ExcelWriter('result.xlsx')
result_df.to_excel(writer,'Sheet1', index=False)
writer.save()
