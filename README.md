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
 * Start solr: `./solr start`
 * You will need a working Java 1.8 JRE to run Solr.
 * Create a core with `./solr create -c <core_name>`
 * Delete the managed-schema file (path would be something like
   /usr/local/solr-6.2.1/server/solr/<core_name>/conf)
 * Copy `import/schema/schema.xml` to the solr conf dir (same as above)
 * In `solrconfig.xml` check/do
   - Remove any ManagedIndexSchemaFactory definition if it exists
   - Add `<schemaFactory class="ClassicIndexSchemaFactory"/>`


### Postgres

```bash
sudo apt-get install postgresql postgresql-contrib 

``` 
Also, dev package needs to be installed, so pip can install 
needed packages as well. The code is given for the current version 9.5.
```bash
sudo apt-get install postgresql-server-dev-9.5
```

Maybe you would like to create postgres user, so you don't have to use
`postgres` automatically created user.

e.g.
```bash
sudo su postgres
createuser --interactive
```
Follow the dialog and create a user with your desired username 
(can be same as the system username). 

You can also do this instead first step, if just want to be able
to create databases:
```bash
createuser desired_username --createdb
```

If you set it up
as admin, maybe you would like to create a DB with the same name.

```bash
psql postgres -U desired_username
```
and then
```postgresql
CREATE DATABASE db_name;
```

### Configuration
There is a `settings.py` file which holds all configuration options to setup
 * Solr Url (default: http://localhost:8983/solr/pacs/query)
 * DCMTK settings (only needed for Download/Transfer)

Create a directory called `instance` in the projects root directory 
and create a file called config.cfg. This holds all instance 
specifying configuration options.

An example would be:
```
DEBUG=False
# Don't show transfer and download options
DEMO=True
SOLR_HOSTNAME='solr'
SOLR_CORE_NAME='grouping'
```

Don't forget to set `DEMO` to `False` if you want to see the download options. 
Without this you will not be able to download the data.

You will also need to get dcm.in DICOM query file from somewhere.

You will also have to fill it with data.

Please note that you will only be able to download images if your machine is 
on the list of allowed machines on the PACS. This means that if you select 
your local machine to be an aet machine, it will act as SCP to receive the 
data. If this is not possible, consider using a remote machine.

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
