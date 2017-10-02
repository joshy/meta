""" Convert new json files and insert ris report """

import json
import requests
from meta.app import app
from timeit import time
from os import walk

new_json = app.config['PATH_TO_MOD_JSON']
# process one month at a time
# First step: convert the original json to one with
# the needed parent-child relation
for (_, _, filenames) in walk(new_json):
    # one json pacs file per month
    for file in filenames:
        with open(new_json + file, 'r+') as blu:
            print('loading ' + new_json + file)
            data = blu.read()
            json_in = json.loads(data)
            json_out = []
            print(len(json_in))
            ts = time.time()
            ctr = 0
            for entry in json_in:
                if ctr==0:
                    tss = time.time()
                ctr = ctr+1
                dic = {}
                dic = entry
                aNum = str(entry['AccessionNumber'])
                t1 = time.time()
                url = app.config['REPORT_SHOW_URL'] + aNum + '&output=text'
                response = requests.get(url)
                data = response.text
                print('t1', time.time() - t1)

                t2 = time.time()
                dic['RisReport'] = data
                json_out.append(dic)
                print('t2', time.time() - t2)
                if ctr==1000:
                    print('1000', time.time() - tss)
                    ctr=0

            print('nach loop', time.time() - ts)  
        
        name = 'rp-' + file
        with open(name, 'w') as fp:
            json.dump(json_out, fp, indent=4)