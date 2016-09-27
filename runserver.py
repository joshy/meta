import os
import logging
from logging.handlers import RotatingFileHandler

from meta import app


LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

handler = RotatingFileHandler('logs/server.log', maxBytes=10000, backupCount=10)
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.run(debug=True, host='0.0.0.0')
