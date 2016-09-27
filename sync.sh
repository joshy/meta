#!/bin/sh
rsync . -avz --exclude logs --exclude __pycache__ -e ssh pacs@10.40.38.52:/Users/pacs/meta