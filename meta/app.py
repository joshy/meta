from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('meta.default_config')
app.config.from_pyfile('config.cfg')
app.config['VERSION'] = '1.1.3'

assets = Environment(app)
js = Bundle("js/jquery-3.1.0.min.js", "js/tether.min.js",
            "js/bootstrap.min.js", "js/moment.min.js", "js/pikaday.js",
            "js/pikaday.jquery.js", "js/jquery.noty.packaged.min.js",
            "js/script.js",
            filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

import meta.views
