"""
DCMTK command generation.
"""

TARGET_MAPPING = {
    'syngo': 'SRSYVMS01',
    'teamplay': 'TEAMPLAY',
    'teamplayshare': 'TEAMPLAY-ISHARE'
}


def construct_transfer_command(dcmkt_config, pacs_config, target, study_id):
    """ Constructs the first part of the transfer command_creator to a PACS node. """
    node = TARGET_MAPPING[target]

    return (
        dcmkt_config.dcmtk_bin +
        'movescu -v -S '
        '-aem {} '
        '-aet {} '
        '-aec {} {} {} '
        '+P {} '
        '-k StudyInstanceUID={} {}'.format(
            node,
            pacs_config.ae_title,
            pacs_config.ae_called,
            pacs_config.peer_address,
            pacs_config.peer_port,
            pacs_config.incoming_port,
            study_id,
            dcmkt_config.dcmin
        )
    )
