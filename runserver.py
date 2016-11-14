"""
Module to run the application. Defines also logging configuration.
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from meta import app


LOG_DIR = os.path.join(os.path.abspath(__file__), 'logs')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

HANDLER = TimedRotatingFileHandler(LOG_DIR, when='midnight', backupCount=10)
HANDLER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
HANDLER.setFormatter(FORMATTER)

app.logger.addHandler(HANDLER)
app.run(debug=True, host='0.0.0.0')
