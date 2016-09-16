import requests
from flask import Flask, render_template, request

# PAGING 
START=0
ROWS=100

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search')
def search():
    searchterm = request.args.get('q')
    url = 'http://localhost:8983/solr/pacs/query?wt=json&start=0&rows=500&q=StudyDescription:' + searchterm
    print(url)
    response = requests.get(url)
    data = response.json()
    docs = data['response']['docs']
    results = data['response']['numFound']
    return render_template('table.html', docs=docs, results=results)