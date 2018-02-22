"""
Default configuration
This can be overwritten with a `instance` folder on the parent level with
a configuration. The configuration file needs to be named 'config.cfg'.
"""

# Application settings
DEBUG = False
RESULT_LIMIT = 100

# Don't show transfer and download options
DEMO = False

# Location of where the image data should be downloaded to (Full path!)
IMAGE_FOLDER = '/home/giga/images'
REPORT_SHOW_URL = 'http://meqpacscrllt01.uhbs.ch:9000/show?accession_number='

# Solr settings
SOLR_HOSTNAME = 'meqpacscrllt01'
SOLR_PORT = '8983'
SOLR_CORE_NAME = 'ris_pacs'

# DCMTK settings
DCMIN = '/home/giga/dev/python/meta/meta/dcm.in'
DCMTK_BIN = '/home/giga/apps/'

AE_TITLE = 'SNOWFOX'
AE_CALLED = 'AE_ARCH2_4PR'
PEER_ADDRESS = '10.5.66.74'
PEER_PORT = 104
INCOMING_PORT = 11110

