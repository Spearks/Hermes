from django.shortcuts import render
from celery.result import AsyncResult   
from hermes.celery import app
from .models import FileExportModel, Channel, DeviceModel
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from hermes.settings import env
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


def home_view(request):
    channels = Channel.objects.all().cache()
    devices = DeviceModel.objects.all().cache()

    context = {
        "channels" : channels,
        "devices" : devices,
        "current_path" : request.path,
    }
    return render(request, "overview.html", context)

def system_view(request):

    context = {
    }
    
    return render(request, "system.html", context)


def devices_view(request, device):
    devices = DeviceModel.objects.all()
    device = devices.get(id=device)
    exports = FileExportModel.objects.all().count
    channels = Channel.objects.all().filter(device=device)

    context = {
        "exports" : exports,
        "channels" : channels,
        "devices" : devices,
        "current_device" : device,
        "current_channels" : channels,
        "current_path" : request.path,
        "grafana_host" : env('GRAFANA_HOST').rstrip(),
        "grafana_port" : env('GRAFANA_PORT').rstrip()
    }

    return render(request, "overview-channel.html", context)

def devices_list_view(request):
    devices = DeviceModel.objects.all()
    context = {
        "devices" : devices,
        "current_path" : request.path,
    }

    return render(request, "devices.html", context)

def channel_view(request, ch):
    channel = Channel.objects.all().filter(id=int(ch))
    context = {
        "channel" : channel[0]
    }

    return render(request, "export.html", context)

def reports_view(request):
    channels = Channel.objects.all()
    context = {
        "channels" : channels
    }
    return render(request, "reports.html", context)

def reports_list_view(request):
    file_exports = FileExportModel.objects.order_by('-created_date')
    context = {
        "files" : file_exports
    }
    return render(request, "reports.html", context)

def sheet_preview(request):

    return render(request, "export/preview_export.html")

from prometheus_api_client.utils import parse_datetime
from app.models import FileExportModel

def channel_list_device(request, device): 
    devices = DeviceModel.objects.all()

    channels = Channel.objects.all().filter(device=device)
    context = {
        "devices" : devices,
        "current_device" : device,
        "current_channels" : channels,
        "current_path" : request.path,
    }

    return render(request, "overview-channel.html", context)

def channels_view_by_device(request, device):
    device = DeviceModel.objects.all().get(id=device)

    channels = Channel.objects.all().filter(device=device)
    context = {
        "current_device" : device,
        "current_channels" : channels,
        "current_path" : request.path,
    }

    return render(request, "channels/channels_list.html", context)

def channel_export_view(request, ch):
    channel = get_object_or_404(Channel, pk=ch)

    print(channel)
    context = {
        "channel" : channel
    }

    return render(request, "export/export_view.html", context)

def multiple_channels_export_view(request):
    channels = request.GET.getlist('channel')

    channels = [ get_object_or_404(Channel, pk=ch) for ch in channels]

    for index, channel in enumerate(channels):
        if channel.device != channels[index - 1].device: return HttpResponseNotFound("Canais com diferentes dispositivos!") 

    context = {
        "channels_export" : channels,
        "current_device" : channels[0].device
    }

    return render(request, "export/export_multiple_channels.html", context)


def channel_export_endpoint(request):
    # if request.method == "GET":
    #     time_values = request.GET.getlist('time')
    #     time_f_values = request.GET.getlist('time-f')
    #     pmin_values = request.GET.getlist('pmin')
    #     channel = request.GET.get('channel')
        
    #     channel =  Channel.objects.get(pk=int(channel))
        
    #     prometheus = channel.device.prefix + '_' + channel.prometheus_name
    #     print(prometheus)
    #     export = []
        
    #     for i in range(0, len(time_values) ):

    #         time_start = parse_datetime(time_values[i] ) 
    #         time_end = parse_datetime(time_f_values[i] ) 
    #         p_min = int(pmin_values[i])

    #         export.append( (time_start, time_end, p_min) )

    #     task = export_metric_data.delay(export, prometheus)

    #     file_exports = FileExportModel.objects.order_by('-created_date')

    #     context = {
    #         "files" : file_exports,
    #         "error" : task.get()["message"] if task.get()["return"] == "Error" else None
    #     }

    return render(request, "reports.html") #, context)
    
@login_required()
def admin_settings_view(request):
    
    context = {

    }

    return render(request, "admin/settings.html", context)  

import datetime
import os
from django.http import JsonResponse
import psutil

# view to get the current server state
# todo: docker status
def server_state(request):
    # Get the system uptime using psutil
    uptime_seconds = psutil.boot_time()
    current_time_seconds = psutil.time.time()
    uptime_delta = current_time_seconds - uptime_seconds

    # Convert the uptime into a human-readable format
    uptime_minutes, uptime_seconds = divmod(uptime_delta, 60)
    uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)
    uptime_days, uptime_hours = divmod(uptime_hours, 24)

    ram = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    server_info = {
        'available_ram' : "%.2f" % round(ram, 2),
        'cpu_percent' : psutil.cpu_percent(),
        'uptime' : {
            'days': int(uptime_days),
            'hours': int(uptime_hours),
            'minutes': int(uptime_minutes),
            'seconds': int(uptime_seconds)
        }

    }

    # Return the uptime information as a JSON response
    return JsonResponse(server_info)
