#!/usr/bin/env sh

set -o errexit
set -o nounset

python /code/manage.py migrate
python /code/manage.py runserver 0.0.0.0:8000
