from meta.settings import *

BASE_COMMAND = DCMTK_BIN \
               + 'movescu -v -S -k QueryRetrieveLevel=SERIES ' \
               + CONNECTION


TRANSFER_COMMAND = DCMTK_BIN \
                   + 'movescu -v -S ' \
                   + TRANSFER_CONNECTION + ' -k QueryRetrieveLevel=STUDY '


def transfer_command(target):
    return DCMTK_BIN + 'movescu -v -S ' \
           + transfer_target(target) + ' -k QueryRetrieveLevel=STUDY '


TARGET_MAPPING = {
    'syngo': 'SRSYVMS01',
    'teamplay': 'TEAMPLAY',
    'teamplayshare': 'TEAMPLAY-ISHARE'
}


def transfer_target(target):
    node = TARGET_MAPPING[target]
    s = Template('-aem $node -aet MC526512B -aec GEPACS 10.247.12.145 4100 +P 4101 $dcmin')
    return s.substitute(node=node, dcmin=DCMIN)
