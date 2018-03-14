import logging
import typing


import pandas as pd
from werkzeug.datastructures import MultiDict

from meta.client.api import SearchParams, query_solr


##
# Example how to use the api to search for someting
# env PYTHONPATH=. python meta/client/example.py
##


# example csv file, provide your own
df = pd.read_csv('accessions.csv')
accs = df['id'].tolist()
accs=list(map(str, accs))

result_df = []
for i in accs:
    params = SearchParams().accession_number(i).build()
    result_df.append(query_solr(params))


writer = pd.ExcelWriter('result.xlsx')
pd.concat(result_df).to_excel(writer,'Sheet1', index=False)
writer.save()
