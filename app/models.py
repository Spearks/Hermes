from django.db import models
import os 
# Create your models here.

class FileExportModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    xlsx_file = models.FileField(upload_to='exported/')
    created_date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.xlsx_file.name)

class DeviceModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(blank=None)
    port = models.PositiveIntegerField()
    grafana_dashboard_name = models.CharField(max_length=64)  

    def __str__(self):
        return self.name

class DashboardService(models.Model):
    id = models.BigAutoField(primary_key=True, blank=False)
    name = models.CharField(max_length=64)


class Channel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    grafana_id = models.PositiveIntegerField()
    desc = models.CharField(max_length=100)
    def __str__(self):
        return self.name