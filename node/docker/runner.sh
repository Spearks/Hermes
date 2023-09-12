#!/bin/bash

poetry shell
    
set -a 
source .env

sleep 15
python /app/node/docker/setup.py 

echo ${GRAFANA_TOKEN}

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


GRAFANA_TOKEN={$GRAFANA_TOKEN} gunicorn hermes.wsgi -b 0.0.0.0 --reload