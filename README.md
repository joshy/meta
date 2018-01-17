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
 * Copy `import/schema/schema.xml` to the solr conf dir
 * In `solrconfig.xml` check/do
   - Remove any ManagedIndexSchemaFactory definition if it exists
   - Add `<schemaFactory class="ClassicIndexSchemaFactory"/>`

### Setup Celery with RabbitMQ
For queuing purposes we will need *Celery* with *RabbitMQ* as a message
broker. Alternative is to use *Redis*, but *RabbitMQ* has been supported
longer and is advertised as more robust in cases of abrupt power outages.

A more in-depth text about why should you use a proper AMPQ instead of DB can
be found [here](https://denibertovic.com/posts/celery-best-practices/).

To install and run *RabbitMQ* on *Ubuntu* based machine, just this in terminal:

```bash
sudo apt-get install rabbitmq-server
```
When the command completes, the broker will already be running in the background,
ready to move messages for you.

To enable management console run:
```bash
sudo rabbitmq-plugins enable rabbitmq_management
```
Now you can access it by going to [http://localhost:15672/]().
Default credentials are `guest:guest`.

For other distros and OSs please check 
[RabbitMQ download page](http://www.rabbitmq.com/download.html).

*TODO: Use [prebuilt docker image for RabbitMQ](https://hub.docker.com/_/rabbitmq/).*

Now we want to start the service (this can also be done in the background):
```bash
celery -c 1 -A <tasks module> worker --loglevel=info
```
The option `-c 1` tells celery to use only one worker.

Install flower to sees celery stats:
```bash
pip install flower
```

For backend (maybe)
```bash
sudo apt-get install redis-server
pip intall redis
```
*TODO: Set redis persistance on each transaction*

### Celery with Postgres

```bash
sudo apt-get install postgresql postgresql-contrib 

``` 
Also, dev package needs to be installed, so pip can install 
needed packages as well. The code is given for the current version 9.5.
```bash
sudo apt-get install postgresql-server-dev-9.5
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
