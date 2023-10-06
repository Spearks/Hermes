#!/bin/bash

sleep 10

poetry shell
    
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

celery -A hermes worker --loglevel=INFO


