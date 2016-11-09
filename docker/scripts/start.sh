#!/bin/bash

uwsgi --ini meta.ini
service nginx start
