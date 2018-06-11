import sqlite3
from datetime import datetime
from flask import Flask, g
from flask_assets import Environment, Bundle

from meta.config import dcmtk_config, pacs_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('meta.default_config')
app.config.from_pyfile('config.cfg', silent=True)

# Exposing constants to use

VERSION = app.config['VERSION'] = '2.3.0'
RESULT_LIMIT = app.config['RESULT_LIMIT']

# DCMTK settings
DCMTK_CONFIG = dcmtk_config(app.config)
PACS_CONFIG = pacs_config(app.config)

OUTPUT_DIR = app.config['IMAGE_FOLDER']
TASKS_DB = app.config['TASKS_DB']
REPORT_SHOW_URL = app.config['REPORT_SHOW_URL']

SHOW_DOWNLOAD_OPTIONS = app.config['SHOW_DOWNLOAD_OPTIONS']
SHOW_TRANSFER_TARGETS = app.config['SHOW_TRANSFER_TARGETS']
TRANSFER_TARGETS = app.config['TRANSFER_TARGETS']

def get_db():
    """ Returns a connection to sqllite db. """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(TASKS_DB, detect_types=sqlite3.PARSE_DECLTYPES)
    return g._database


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes DB connection when app context is done. """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

init_db()


@app.template_filter('to_date')
def to_date(date_as_int):
    if date_as_int:
        return datetime.strptime(str(date_as_int), '%Y%m%d').strftime('%d.%m.%Y')
    else:
        return ''


# JS Assets part
assets = Environment(app)
js = Bundle("js/jquery-3.1.0.min.js", "js/tether.min.js",
            "js/bootstrap.min.js", "js/moment.min.js", "js/pikaday.js",
            "js/pikaday.jquery.js", "js/jquery.noty.packaged.min.js",
            "js/jszip.min.js", "js/FileSaver.js", "js/script.js",
            filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

import meta.views
