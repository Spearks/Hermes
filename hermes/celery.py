import os

from celery import Celery
from .settings import env

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hermes.settings')

result_backend = env('RBMQ_CELERY_BROKER_URL').replace('amqp://', 'rpc://')

app = Celery('hermes', broker = env('RBMQ_CELERY_BROKER_URL'), backend=result_backend)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


