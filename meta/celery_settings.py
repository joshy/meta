#CELERY_BROKER_URL = 'amqp://'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TRACK_STARTED = True
BROKER_TRANSPORT = "sqlakombu.transport.Transport"
CELERY_BROKER_URL = "sqla+postgresql://postgres:postgres@localhost/postgres"
CELERY_RESULT_BACKEND = "db+postgresql://postgres:postgres@localhost/postgres"
CELERYD_TASK_TIME_LIMIT = 5 # If not completed in 300 seconds, kill the worker

# Enabling the next two setting can lead to infinite loops and zombie apocalypse

# Enable this to retry if worker fails for some reason
# TASK_ACKS_LATE = True

# Enable this if acks_late is enabled and you want to retry on worker_lost
# TASK_REJECT_ON_WORKER_LOST = True
