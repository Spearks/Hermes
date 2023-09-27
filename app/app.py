from django.apps import AppConfig
from .models import DeviceModel



class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        pass

