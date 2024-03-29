#!/bin/bash
poetry shell
export $(grep -v '^#' .env | xargs)

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput
python node/docker/setup.py

GRAFANA_TOKEN={$GRAFANA_TOKEN} gunicorn hermes.wsgi -b 0.0.0.0 --reload