# A meta crawler for PACS
[![Build Status](https://api.travis-ci.org/joshy/meta.svg?branch=master)](https://travis-ci.org/joshy/meta)

## Purpose
This web application lets the user search through a PACS meta data. The data
needs to be stored on a Apache Solr instance.


## Running the application

### Installation
To run the application, python 3.6 is needed. To manage the python environment
[Anaconda](https://www.continuum.io/downloads) is the recommended way to manage
different python versions.

Python libraries needed are noted in the requirements.txt

### Setup Solr
 * Install solr, see the [Solr website](http://lucene.apache.org/solr/) on how
 to do it
 * Create a core with `solr create -c <core_name>`
 * Delete the managed-schema file (path would be something like
   /usr/local/solr-6.2.1/server/solr/<core_name>/conf)
 * In `solrconfig.xml` check/do
   - Remove any ManagedIndexSchemaFactory definition if it exists
   - Add `<schemaFactory class="ClassicIndexSchemaFactory"/>`

### Configuration
There is a `settings.py` file which holds all configuration options to setup
 * Solr Url (default: http://localhost:8983/solr/pacs/query)
 * DCMTK settings (only needed for Download/Transfer)

Create a directory called `instance` and create a file called config.cfg.
This holds all instance specifig configuration options.

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

#### Run development mode
Another option is to use [nodemon](http://nodemon.io/) which also allows to
reload on changes. The advantage is that even with compile errors the nodemon
is still able to reload while the flask dev server crashes and needs to be
manually restarted. To run with nodemon run
```
./run-dev.sh
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
