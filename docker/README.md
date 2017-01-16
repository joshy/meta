# Docker

## Introduction
This docker-compose configuration sets up two containers. One container will
be the solr container and the other container will run the application.

The solr container creates a core, imports the schema and has some initial
test data in it.

The application container runs nginx, uwsgi and the application. All of those
is supervised with supervisord.

## Setup
To use it, docker-compose (version needs to be > 1.4.0) needs to be installed.
To run it use
```
docker-compose up
```

To stop it use
```
docker-compose down
```

## Running on an EC2 (or similar instance)

```bash
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
curl -L https://github.com/docker/compose/releases/download/1.7.0/docker-compose-`uname -s`-`uname -m` > ./docker-compose
sudo mv ./docker-compose /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
sudo yum install -y git
git clone https://github.com/joshy/meta.git
cd meta/docker/
docker-compose up -d
```
