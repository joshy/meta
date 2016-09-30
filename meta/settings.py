# Solr settings
SOLR_URL = 'http://localhost:8983/solr/pacs/query'


from string import Template

# DCMTK settings
DCMIN = '/Applications/dcmtk/dcm.in'
DCMTK_BIN = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/'

CONNECTION = '-aet YETI  -aec AE_ARCH2_4PR 10.5.66.74 104 +P 11112 ' + DCMIN
TRANSFER_CONNECTION = '-aem SRSYVMS01 -aet MC526512B -aec GEPACS 10.247.12.145 4100 +P 4101 ' + DCMIN
OUTPUT_DIR = 'image_data'


