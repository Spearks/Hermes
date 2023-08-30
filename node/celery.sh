#!/bin/bash

sleep 1

poetry shell
    
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# if [[ "$RUNNER" == "gunicorn" ]]; then
#     echo "Node set to gunicorn"
#     gunicorn hermes.wsgi -b 0.0.0.0 --reload
# elif [[ "$RUNNER" == "celery" ]]; then
#     echo "Node set to django"
#     celery --app hermes worker
# else
#     echo "Runner not defined"
# fi

celery -A hermes worker --loglevel=INFO
