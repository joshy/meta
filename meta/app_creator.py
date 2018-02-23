from datetime import datetime
from flask import Flask
import configparser
from os.path import join, dirname
from flask_assets import Environment
from webassets import Bundle


def _to_date(date_as_int):
    if date_as_int:
        return datetime.strptime(str(date_as_int), '%Y%m%d').strftime('%d.%m.%Y')
    else:
        return ''


def create_app(config_object_path='meta.default_config',
               config_pyfile_path='config.cfg',
               db_uri=None,
               testing=None,
               server_name=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_object_path)
    app.config.from_pyfile(config_pyfile_path, silent=True)

    app.config['VERSION'] = '2.0.0'

    if server_name is not None:
        app.config['SERVER_NAME'] = server_name

    if testing:
        app.config['TESTING'] = testing
        app.test_client()

    if db_uri is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    config = configparser.ConfigParser()
    with open(join(dirname(__file__), '..', 'luigi.cfg')) as f:
        config.read_file(f)

    app.config['LUIGI_SCHEDULER'] = ':'.join(
        [
            config['core']['default-scheduler-host'],
            config['core']['default-scheduler-port']
        ]
    )

    # JS Assets part
    assets = Environment(app)
    js = Bundle("js/jquery-3.1.0.min.js", "js/tether.min.js",
                "js/bootstrap.min.js", "js/moment.min.js", "js/pikaday.js",
                "js/pikaday.jquery.js", "js/jquery.noty.packaged.min.js",
                "js/script.js",
                filters='jsmin', output='gen/packed.js')
    assets.register('js_all', js)

    app.jinja_env.filters['to_date'] = _to_date

    app.app_context().push()

    return app