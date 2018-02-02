"""
Module to run the application. Defines also logging configuration.
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from meta.app_creator import create_app

app = create_app()

if not app.debug:
    LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'server.log')

    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)

    HANDLER = TimedRotatingFileHandler(LOG_FILE, when='midnight', backupCount=10)
    HANDLER.setLevel(logging.DEBUG)

    FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    HANDLER.setFormatter(FORMATTER)
    app.logger.addHandler(HANDLER)


app.run(host='0.0.0.0', threaded=True)
