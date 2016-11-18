# Docker

## Introduction
This docker-compose configuration sets up two containers. One container will
be the solr container and the other container will run the application.

The solr container creates a core, imports the schema and has some initial
test data in it.

The application container runs nginx, uwsgi and the application. All of those
is supervised with supervisord.

## Setup
To use it, docker-compose needs to be installed. To run it use
```
docker-compose up
```

To stop it use
```
docker-compose down
```