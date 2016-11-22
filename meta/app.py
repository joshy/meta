from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg')
app.config['VERSION'] = '1.0.0'

import meta.views
