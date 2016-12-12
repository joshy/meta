from meta.settings import DCMTK_BIN, CONNECTION, DCMIN


def base_command():
    return DCMTK_BIN \
               + 'movescu -v -S -k QueryRetrieveLevel=SERIES ' \
               + CONNECTION


TARGET_MAPPING = {
    'syngo': 'SRSYVMS01',
    'teamplay': 'TEAMPLAY',
    'teamplayshare': 'TEAMPLAY-ISHARE'
}


def transfer_command(target):
    """ Constructs the first part of the transfer command to a PACS node. """
    return DCMTK_BIN + 'movescu -v -S ' \
           + _transfer_target(target) + ' -k QueryRetrieveLevel=STUDY '


def _transfer_target(target):
    node = TARGET_MAPPING[target]
    return '-aem {} -aet MC526512B -aec GEPACS ' \
           '10.247.12.145 4100 +P 4101 {}'.format(node, DCMIN)
