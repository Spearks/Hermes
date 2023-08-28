from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import DeviceModel

@receiver(post_save, sender=DeviceModel)
def reciver_device(sender, instance, created, **kwargs):
    # Your code here
    if created:
        print("created")
    else:
        print("ok")