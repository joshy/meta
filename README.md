# A meta crawler for PACS

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


### Run
To run the application run
```
python runserver.python
```
this will also automatically reload on changes made.
The application will the accessible on port 5000 with default settings.

### Run tests
```
python -m unittest
```