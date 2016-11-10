#!/bin/bash
source activate python35
uwsgi --ini meta.ini &
service nginx start
