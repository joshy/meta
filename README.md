# A meta crawler for PACS
[![Build Status](https://api.travis-ci.org/joshy/meta.svg?branch=master)](https://travis-ci.org/joshy/meta)

## Purpose
This web application lets the user search through a PACS meta data. The data
needs to be stored on a Apache Solr instance.


## Running the application

### Python Installation and virtual environments
To run the application, python 3.6 is needed. To manage the python environment
[Anaconda](https://www.continuum.io/downloads) is the recommended way to manage
different python versions. Install it and add it to your path.

Create virtual environment with conda:
```bash
conda create -n meta --no-default-packages python=3.6
```

And activate the environment:
```bash
source activate meta
```

Now install all the requirements:
```bash
pip install -r requirements.txt
```
Python libraries needed are listed in the file requirements.txt

You now have a correctly set up Python environment.


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

You will be able to connect to the database with the username `postgres` and an emtpy password.

If your empty password produces and error, try setting the password to something e.g. `postgres`
(see [changing the password](#changing-the-password)).

After this, the connection string should contain 'postgres:postgres' as the user and the password
and the database `postgres`.


#### Creating a user

Skip this part if you are not sure that you need it.

Follow these steps if you would like to create a new postgres user, so you don't have to use the default one
(`postgres`).

e.g.
```bash
sudo su postgres
createuser --interactive
```
Follow the dialog and create a user with your desired username
(can be same as the system username).

Alternatively, if just want to be able
to create databases, do this:
```bash
createuser desired_username --createdb
```

#### Changing the password
To set the password for the newly created user do:
```bash
psql -U postgres
ALTER USER username WITH PASSWORD 'new_password';
```

#### Creating the admin database for the user
If you set up the new user as admin, you might want to create a DB with the same name (case sensitive).

```bash
psql postgres -U username --host localhost
```
and then
```postgresql
CREATE DATABASE username;
```

### Luigi
We are using Luigi to schedule tasks. You need to run the local scheduler first.
Navigate to the root of the project or wherever your `luigi.cfg` file is, and run:
```bash
luigid
```

Go [here](#luigi-config) for more information about the configuration file.

### Configuration

#### General config
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

You will also need to get dcm.in DICOM query file from somewhere
and you will have to fill it with data.

Please note that you will only be able to download images if your machine is
on the list of allowed machines on the PACS. This means that if you select
your local machine to be an aet machine, it will act as SCP to receive the
data. If this is not possible, consider using a remote machine.

#### Luigi config

Luigi config file, named `luigi.cfg`, is located in the root of the project.

By default the config is set to store history. It is using SQLAlchemy for that,
so you can provide any of the supported connection strings.
The template already contains an example for the postgres connection string.

Please note that databases other than postgres might require you to take care of dependencies.

Core information is also used by flask, so that you are redirected correctly to the
luigi scheduler web page.


### Run
After you have completed all of the steps, proceed with the following command:
```bash
python runserver.python
```

If something goes wrong, please check that you have done everything on this check list:
* [Setup Python and switch to correct virtual environment](#python-installation-and-virtual-environments)
* [Install and run solr](#setup-solr)
* [Install and run postgress](#postgres)
* [Run Luigi scheduler](#luigi)
* [Check config](#configuration)

#### Run development mode
Another option is to use [nodemon](http://nodemon.io/) which also allows to
reload on changes. The advantage is that even with compile errors the nodemon
is still able to reload while the flask dev server crashes and needs to be
manually restarted. To run with nodemon run
```bash
./run-dev.sh
```


### Run tests and coverage
```bash
python -m unittest
coverage run --source=. -m unittest

# generate console reports
coverage report

# generate html reports
coverage html -d coverage
```

### uWSGI

The pip install might throw an error when you try to install uwsgi.
Installation from conda-forge works for now without any issues. To install
from conda-forge run:
```bash
conda install -c conda-forge uwsgi
```
Be careful that it does not break your pip dependencies.

You can now call `uwsgi` with the accompanying `meta.ini` file.


### Production
Increase open file limit
https://easyengine.io/tutorials/linux/increase-open-files-limit/