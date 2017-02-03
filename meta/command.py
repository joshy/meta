from meta.app import DCMTK_BIN, DCMIN, AE_TITLE, AE_CALLED, \
                     PEER_PORT, INCOMING_PORT, PEER_ADDRESS


CONNECTION = '-aet {} -aec {} {} {} +P {}'.format(AE_TITLE, AE_CALLED, \
             PEER_ADDRESS, PEER_PORT, INCOMING_PORT)


def base_command():
    return DCMTK_BIN \
               + 'movescu -v -S -k QueryRetrieveLevel=SERIES ' \
               + CONNECTION


TARGET_MAPPING = {
    'syngo': 'SRSYVMS01',
    'teamplay': 'TEAMPLAY',
    'teamplayshare': 'TEAMPLAY-ISHARE'
}


def _transfer_part(node, study_id):
    return '-aem {} -aet {} -aec {} {} {} +P {} -k StudyInstanceUID={} {}' \
                        .format(node, AE_TITLE, AE_CALLED, PEER_ADDRESS, \
                        PEER_PORT, INCOMING_PORT, study_id, DCMIN)


def transfer_command(target, study_id):
    """ Constructs the first part of the transfer command to a PACS node. """
    return DCMTK_BIN + 'movescu -v -S ' \
           + _transfer_target(target, study_id)


def _transfer_target(target, study_id):
    node = TARGET_MAPPING[target]
    return _transfer_part(node, study_id)
