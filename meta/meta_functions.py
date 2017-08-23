""" Helper functions to crawl """

import requests

def test_query(params):
    """ Query im ris
    """
    q_in = params.get('query')
    core = 'http://localhost:8983/solr/ris_crawler/select?'
    rows_in = '1'
    rows_out = '&rows=' + rows_in
    q_out = '&q=' + q_in

    go_for_it = core + '&wt=json' + q_out + rows_out
    print(go_for_it)
    res = requests.get(go_for_it)
    response = res.json()
    dicts = response['response']
    rows_in = dicts['numFound']
    rows_out = '&rows=' + str(rows_in)
    go_for_it = core + '&wt=json' + q_out + rows_out
    res = requests.get(go_for_it)
    response = res.json()
    dicts = response['response']
    dict_of_docs = dicts['docs']
    # evtl nume d liste vo acc num zrugg geh
    # accNum = [] 
    # for entry in dict_of_docs:
    #     accNum.append(entry['unters_schluessel'])
    # return accNum

    return dict_of_docs

def merge_queries(pacs_response, ris_response, payload):
    """ Get the results, based on the accession number, from both queries and return 
        the merged array of accession numbers (to feed in the pacs again for display)
    """
    ctr = 0
    data = pacs_response.json()
    docs = data['grouped']['PatientID']['groups']

    # 1. Schlaufe über Resultat vom pacs
    acc_num = ''
    for doc in docs:
        acc_num = acc_num + ', ' + str(doc['doclist']['docs'][0]['AccessionNumber'])
        ctr += 1

    # 2. Schlaufe über Resultat vom ris
    # Werde nur derzue gmacht wenn nit scho in de pacs Resultat drin
    for entry in ris_response:
        if str(entry['unters_schluessel']) not in acc_num:
            acc_num = acc_num + ', ' + str(entry['unters_schluessel'])
            ctr += 1
    acc_num = acc_num[2:len(acc_num)]

    # 'payload' wird neu uf alli gfundene accession numbers gsetzt
    # und es wird neu im pacs gsuecht
    payload['query'] = acc_num
