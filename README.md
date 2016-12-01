# A meta crawler for PACS
[![Build Status](https://api.travis-ci.org/irrwitz/meta.svg?branch=master)](https://travis-ci.org/irrwitz/meta)
## Purpose
This web application lets the user search through a PACS meta data. The data
needs to be stored on a Apache Solr instance.


## Running the application

### Installation
To run the it, python 3.5 is needed. To manage the python environment
[Anaconda](https://www.continuum.io/downloads) should be used.

Python libraries needed are:
 * Flask
 * requests

### Configuration
There is a `settings.py` file which holds all configuration options to setup
 * Solr Url (default: http://localhost:8983/solr/pacs/query)
 * DCMTK settings (only needed for Download/Transfer)

On the same level as meta, doc and so on directory called `instance` should be
created with a file called config.cfg. This holds all instance specifig
configuration options which should not be overwritten by updates.
An example would be:
```
DEBUG=False
# Don't show transfer and download options
DEMO=True
SOLR_HOSTNAME='solr'
SOLR_CORE_NAME='grouping'
```


### Run
To run the application run
```
python runserver.python
```
this will also automatically reload on changes made.
The application will the accessible on port 5000 with default settings.
Another option is to use [nodemon](http://nodemon.io/) which also allows to
reload on changes. The advantage is that even with compile errors the nodemon
is still able to reload while the flask dev server crashes and needs to be
manually restarted. To run with nodemon run
```
nodemon --exec "python" runserver.py
```


### Run tests and coverage
```
python -m unittest
coverage run --source=. -m unittest

# generate console reports
coverage report

# generate html reports
coverage html -d coverage
```
