from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('meta.default_config')
print(app.config['DEBUG'])
app.config.from_pyfile('config.cfg')
print(app.config['DEBUG'])
app.config['VERSION'] = '1.0.0'

import meta.views
