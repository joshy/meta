from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('meta.default_config')
app.config.from_pyfile('config.cfg', silent=True)

# Exposing constants to use
DEMO = app.config['DEMO']
VERSION = app.config['VERSION'] = '1.3.2'
RESULT_LIMIT = app.config['RESULT_LIMIT']

# DCMTK settings
DCMTK_BIN = app.config['DCMTK_BIN']
DCMIN = app.config['DCMIN']
AE_TITLE = app.config['AE_TITLE']
AE_CALLED = app.config['AE_CALLED']
PEER_ADDRESS = app.config['PEER_ADDRESS']
PEER_PORT = app.config['PEER_PORT']
INCOMING_PORT = app.config['INCOMING_PORT']


OUTPUT_DIR = app.config['IMAGE_FOLDER']

# JS Assets part
assets = Environment(app)
js = Bundle("js/jquery-3.1.0.min.js", "js/tether.min.js",
            "js/bootstrap.min.js", "js/moment.min.js", "js/pikaday.js",
            "js/pikaday.jquery.js", "js/jquery.noty.packaged.min.js",
            "js/script.js",
            filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

import meta.views
