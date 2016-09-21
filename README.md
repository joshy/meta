# A meta crawler for PACS

## Purpose
This web application lets the user search through a PACS meta data. This data 
needs to be stored on a Apache Solr instance.


## Running the application

### Installation
To run the it, python 3.5 is needed. To manage the python environment 
[Anaconda](https://www.continuum.io/downloads) should be used.


### Configuration 
There is a `settings.py` file which holds all configuration options to setup
 * Solr Url
 * DCMTK settings


### Run
To run the application run
```
python runserver.python
```
this will also automatically reload on changes made. 

