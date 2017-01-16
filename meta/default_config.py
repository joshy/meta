"""
Default configuration
This can be overwritten with a `instance` folder on the parent level with
a configuration. The configuration file needs to be named 'config.cfg'.
"""

# Application settings
DEBUG = False
RESULT_LIMIT = 100

## Don't show transfer and download options
DEMO = True

## Location of where the image data should be donwloaded to (Full path!)
IMAGE_FOLDER = '/Users/joshy/github/meta/image_data'

# Solr settings
SOLR_HOSTNAME = 'localhost'
SOLR_CORE_NAME = 'grouping'

# DCMTK settings
DCMIN = '/Applications/dcmtk/dcm.in'
DCMTK_BIN = '/Applications/dcmtk/dcmtk-3.6.0-mac-i686-dynamic/bin/'
