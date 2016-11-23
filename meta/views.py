import json
from requests import get

from flask import render_template, request, redirect, url_for

import meta.query
from meta.app import app
from meta.pull import download_series, transfer_series
from meta.paging import calc
from meta.facets import prepare_facets
from meta.grouping import group
from meta.solr import solr_url
from meta.terms import get_data


@app.route('/')
def main():
    """ Renders the initial page. """
    return render_template('search.html', version=app.config['VERSION'],
                           params={'query': '*:*'})


@app.route('/search')
def search():
    """ Renders the search results. """
    params = request.args
    payload = meta.query.query_body(params)
    headers = {'content-type': "application/json"}
    response = get(solr_url(), data=json.dumps(payload), headers=headers)
    app.logger.debug('Calling Solr with url %s', response.url)
    app.logger.debug('Request body %s', json.dumps(payload))
    try:
        if response.status_code == 400 or response.status_code == 500:
            result = response.json()
            error = result['error']
            msg = result['error']['msg']
            trace = error.get('trace', '')

            return render_template('search.html',
                                   params={},
                                   error=' Call to Solr failed: ' + msg,
                                   trace=trace)
        data = response.json()
        docs = data['grouped']['PatientID']
        docs = group(docs)
        facets = prepare_facets(data.get('facets', []), request.url)
        results = data['grouped']['PatientID']['ngroups']
        paging = calc(results, request.url, params.get('offset', '1'))
        demo = app.config['DEMO']
        print(demo)
        return render_template('result.html',
                               docs=docs,
                               results=results,
                               facets=facets,
                               payload=payload,
                               facet_url=request.url,
                               params=params,
                               paging=paging,
                               version=app.config['VERSION'],
                               modalities=params.getlist('Modality'),
                               demo=demo)
    except json.JSONDecodeError:
        return render_template('search.html',
                               params={},
                               error='Can\'t decode JSON, is Solr running?')


@app.route('/download', methods=['POST'])
def download():
    """ Ajax post to download series of images. """
    app.logger.info("download called")
    data = request.get_json(force=True)
    series_list = data.get('data', '')
    dir_name = data.get('dir', '')
    download_series(series_list, dir_name)
    return 'OK'


@app.route('/transfer/<target>', methods=['POST'])
def transfer(target):
    """ Ajax post to transfer series of images to another PACS node. """
    app.logger.info("transfer called and sending to %s", target)
    series_list = request.get_json(force=True)
    transfer_series(series_list, target)
    return 'OK'


@app.route('/terms')
def terms():
    """ Renders a page about term information. Only internal use. """
    app.logger.info("Terms called")
    data = get_data()
    return render_template('terms.html', terms=data)


@app.route('/settings')
def settings():
    """ Renders a page where the user can change the core to connect to. """
    app.logger.info("Settings called")
    return render_template('settings.html', core_name=app.config['SOLR_CORE_NAME'])


@app.route('/settings', methods=['POST'])
def set_core():
    """ Changes the core to connect to. """
    core_name = request.form['core_name']
    app.logger.info("Setting core to %s", core_name)
    app.config.update(SOLR_CORE_NAME=core_name)
    return redirect(url_for('main'))
