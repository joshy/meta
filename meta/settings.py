# Interface to configuration options
from meta.app import app

RESULT_LIMIT = app.config['RESULT_LIMIT']

# DCMTK settings
DCMTK_BIN = app.config['DCMTK_BIN']
DCMIN = app.config['DCMIN']
AE_TITLE = app.config['AE_TITLE']
CONNECTION = '-aet ' + AE_TITLE + ' -aec AE_ARCH2_4PR 10.5.66.74 104 +P 11112 ' + DCMIN

OUTPUT_DIR = app.config['image_data']
