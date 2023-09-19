from django.utils import timezone
from grafanalib.formatunits import (
    MILLI_METER,
    KILO_GRAM,
    BARS,
    KILO_BARS,
    PASCALS,
    PSI    
)
from django.db import models
import os 
# Create your models here.

class FileExportModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    xlsx_file = models.FileField(upload_to='exported/')
    created_date = models.DateTimeField(auto_now_add=True)
    lines = models.BigIntegerField(default=0)

    def filename(self):
        return os.path.basename(self.xlsx_file.name)

class DeviceModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=64)

    prefix = models.CharField(max_length=12)
    ip = models.GenericIPAddressField(blank=None)
    port = models.PositiveIntegerField()

    online = models.BooleanField(default=False)
    last_online = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class DashboardService(models.Model):
    id = models.BigAutoField(primary_key=True, blank=False)
    name = models.CharField(max_length=64)

class Channel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)

    prometheus_name = models.CharField(max_length=64)
    online = models.BooleanField(default=False)

    UNIT_CHOICES = [
        (MILLI_METER, 'Millimeter'),
        (KILO_GRAM, 'Kilogram'),
        (BARS, 'Bars'),
        (KILO_BARS, 'Kilobars'),
        (PASCALS, 'Pascals'),
        (PSI, 'PSI'),
    ]

    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)

    def __str__(self):
        return self.name


import app.signals