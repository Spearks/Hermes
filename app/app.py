from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):

        from app.models import DeviceModel
        
        for Device in DeviceModel.objects.all():
            print(Device)