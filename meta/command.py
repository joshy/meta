"""
DCMTK command generation.
"""

TARGET_MAPPING = {
    'syngo': 'SRSYVMS01',
    'teamplay': 'TEAMPLAY',
    'teamplayshare': 'TEAMPLAY-ISHARE'
}


def transfer_command(dcmkt_config, pacs_config, target, study_id):
    """ Constructs the first part of the transfer command to a PACS node. """
    return dcmkt_config.dcmtk_bin + 'movescu -v -S ' \
           + _transfer(dcmkt_config, pacs_config, target, study_id)


def base_command(dcmtk_config, pacs_config):
    """ Constructs the first part of a dcmtk command. """
    return dcmtk_config.dcmtk_bin \
               + 'movescu -v -S -k QueryRetrieveLevel=SERIES ' \
               + '-aet {} -aec {} {} {} +P {}'.format(pacs_config.ae_title, \
               pacs_config.ae_called, pacs_config.peer_address, \
               pacs_config.peer_port, pacs_config.incoming_port)


def _transfer(dcmkt_config, pacs_config, target, study_id):
    node = TARGET_MAPPING[target]
    return '-aem {} -aet {} -aec {} {} {} +P {} -k StudyInstanceUID={} {}' \
            .format(node, pacs_config.ae_title, pacs_config.ae_called, \
            pacs_config.peer_address, pacs_config.peer_port, \
            pacs_config.incoming_port, study_id, dcmkt_config.dcmin)
