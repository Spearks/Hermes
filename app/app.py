from django.apps import AppConfig
from django.db.models.signals import post_save
from .signals import reciver_device
from .models import DeviceModel



class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals 

