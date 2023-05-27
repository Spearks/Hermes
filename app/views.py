from django.shortcuts import render
from .tasks import export_metric_data
from celery.result import AsyncResult   
from hermes.celery import app
from datetime import datetime, timedelta
from .models import FileExportModel, Channel, DeviceModel
# Create your views here.

def home_view(request):
    channels = Channel.objects.all()

    context = {
        "channels" : channels
    }
    return render(request, "index.html", context)


def system_view(request):

    context = {
    }
    
    return render(request, "system.html", context)


def devices_view(request):
    devices = DeviceModel.objects.all()
    context = {
        "devices" : devices
    }

    return render(request, "devices.html", context)

def channel_view(request, ch):
    print(ch)
    context = {

    }

    return render(request, "channel.html", context)

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
    return render(request, "reports-list.html", context)

from prometheus_api_client.utils import parse_datetime
from app.models import FileExportModel
from .tasks import export_metric_data

def channel_export_view(request):
    if request.method == "GET":
        time_values = request.GET.getlist('time')
        time_f_values = request.GET.getlist('time-f')
        pmin_values = request.GET.getlist('pmin')
        
        export = []
        
        for i in range(0, len(time_values) ):

            time_start = parse_datetime(time_values[i] ) 
            time_end = parse_datetime(time_f_values[i] ) 
            p_min = int(pmin_values[i])

            export.append( (time_start, time_end, p_min) )

        export_metric_data.delay(export)

        file_exports = FileExportModel.objects.order_by('-created_date')
        context = {
            "files" : file_exports
        }

        return render(request, "reports-list.html", context)
    

