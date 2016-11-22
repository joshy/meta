from meta import app

def solr_url():
    """ Returns the solr url.
    Core name and host are taking from configuration which is in the
    instance/config.cfg
    file.
    """
    core_name = app.config['SOLR_CORE_NAME']
    hostname = app.config['SOLR_HOSTNAME']
    return 'http://{0}:8983/solr/{1}/query'.format(hostname, core_name)


def solr_terms_url():
    """ Returns the solr base url.
    Core name and host are taking from configuration which is in the
    instance/config.cfg
    file.
    """
    core_name = app.config['SOLR_CORE_NAME']
    hostname = app.config['SOLR_HOSTNAME']
    return 'http://{0}:8983/solr/{1}/terms'.format(hostname, core_name)
