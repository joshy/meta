from meta.app import DCMTK_BIN, CONNECTION, DCMIN, AE_TITLE


def base_command():
    return DCMTK_BIN \
               + 'movescu -v -S -k QueryRetrieveLevel=SERIES ' \
               + CONNECTION


TARGET_MAPPING = {
    'syngo': 'SRSYVMS01',
    'teamplay': 'TEAMPLAY',
    'teamplayshare': 'TEAMPLAY-ISHARE'
}


def transfer_command(target, study_id):
    """ Constructs the first part of the transfer command to a PACS node. """
    return DCMTK_BIN + 'movescu -v -S ' \
           + _transfer_target(target, study_id)


def _transfer_target(target, study_id):
    node = TARGET_MAPPING[target]
    return '-aem {} -aet {} -aec GE ' \
           '10.247.12.5 4100 +P 4101' \
           ' -k StudyInstanceUID={} {}'.format(node, AE_TITLE, study_id, DCMIN)
