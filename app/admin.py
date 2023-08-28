from django.contrib import admin
from .models import DeviceModel, Channel, FileExportModel
# Register your models here.

@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Channel)
class ChannelModelAdmin(admin.ModelAdmin):
    pass

@admin.register(FileExportModel)
class FileExportModelAdmin(admin.ModelAdmin):
    pass
