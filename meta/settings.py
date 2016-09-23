# Solr settings
SOLR_URL = 'http://localhost:8983/solr/pacs/query'


# DCMTK settings
DCMIN = "/Applications/dcmtk/dcm.in"
DCMTK_BIN = "/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/"
CONNECTION = "-aet YETI  -aec AE_ARCH2_4PR 10.5.66.74 104 +P 11112 " + DCMIN
BASE_COMMAND = DCMTK_BIN \
               + "/movescu -v -S -k QueryRetrieveLevel=SERIES " \
               + CONNECTION
OUTPUT_DIR = "image_data"
