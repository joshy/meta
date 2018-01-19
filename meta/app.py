from datetime import datetime
from flask import Flask, g
from flask_assets import Environment, Bundle

from meta.config import dcmtk_config, pacs_config

from meta.queue_manager_models import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('meta.default_config')
app.config.from_pyfile('config.cfg', silent=True)

app.app_context().push()
db.init_app(app)
db.create_all()
db.session.commit()

# Exposing constants to use
DEMO = app.config['DEMO']
VERSION = app.config['VERSION'] = '1.5.2'
RESULT_LIMIT = app.config['RESULT_LIMIT']

# DCMTK settings
DCMTK_CONFIG = dcmtk_config(app.config)
PACS_CONFIG = pacs_config(app.config)

OUTPUT_DIR = app.config['IMAGE_FOLDER']
TASKS_DB = app.config['TASKS_DB']
REPORT_SHOW_URL = app.config['REPORT_SHOW_URL']


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
            "js/script.js",
            filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

import meta.views
