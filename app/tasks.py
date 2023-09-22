from prometheus_api_client import PrometheusConnect, MetricsList
from prometheus_api_client.utils import parse_datetime
import pandas as pd
from app.models import FileExportModel
from hermes.celery import app
import random
from django.conf import settings
import os 
from django.core.files.base import File
from hermes.settings import env
from .models import DeviceModel, Channel
import requests

from grafanalib.core import (
    Dashboard, TimeSeries, SingleStat, Row,
    Target, GridPos,
    OPS_FORMAT,
    SHORT_FORMAT,
    YAxes,
    YAxis
)
from grafanalib import formatunits 
from grafanalib._gen import DashboardEncoder
import json
from promql_parser import parse

prom = PrometheusConnect(url =f"http://{env('PROMETHEUS_HOST')}:{env('PROMETHEUS_PORT')}", disable_ssl=True)

@app.task
def discover_channels(device_id):
    device = DeviceModel.objects.all().get(id=device_id)
    
    ip = device.ip
    port = str(device.port) 

    channels = Channel.objects.all().filter(device=device)

    data = requests.get(f"http://{ip}:{port}/api/v1/metrics").json()
    channel_names = []

    if data["status"] == "success":
   
        channel_names = [key for key in data["data"][0].keys() if key.startswith(device.prefix)]
    else:
        raise Exception("Task Discover_channels failed, request was not successful")
        
    for channel in channels:

        if device.prefix + '_' + channel.prometheus_name in channel_names:
            channel.online = True
        else:
            channel.online = False
    

        channel.save()

@app.task
def update_dashboard():
    devices = DeviceModel.objects.all()

    for Device in devices: 
        Channels = Channel.objects.all().filter(device=Device)

        panels = []
        
        for channel in Channels:
            panels.append(
                TimeSeries(
                    title=channel.name, 
                    dataSource='default', 
                    targets=[
                        Target(
                            datasource='default', 
                            expr=Device.prefix + '_' + channel.prometheus_name
                        )
                    ],
                    gridPos=GridPos(h=8, w=16, x=0, y=0),
                    unit=channel.unit
                )
            )
            
            avg_panel = SingleStat(
                title=f"{channel.name} Average",
                dataSource='default',
                targets=[
                    Target(
                        expr=f'avg_over_time({Device.prefix}_{channel.prometheus_name}[$__interval])',
                        legendFormat='Average',
                    ),
                ],
                span=4,
            )

            max_panel = SingleStat(
                title=f"{channel.name} Maximum",
                dataSource='default',
                targets=[
                    Target(
                        expr=f'max_over_time({Device.prefix}_{channel.prometheus_name}[$__interval])',
                        legendFormat='Maximum',
                    ),
                ],
                span=4,
            )

            min_panel = SingleStat(
                title=f"{channel.name} Minimum",
                dataSource='default',
                targets=[
                    Target(
                        expr=f'min_over_time({Device.prefix}_{channel.prometheus_name}[$__interval])',
                        legendFormat='Minimum',
                    ),
                ],
                span=4,
            )

            panels.extend([avg_panel, max_panel, min_panel])

        dashboard = Dashboard(
            title=Device.name,
            description=Device.desc,
            tags=['hermes-auto-generated'],
            timezone="browser",
            rows=[Row(panels=panels)]
        ).auto_panel_ids()

        pretty_json = json.dumps(dashboard.to_json_data(), sort_keys=True, indent=2, cls=DashboardEncoder)
        
        api_key = env('GRAFANA_TOKEN')
        server = env('GRAFANA_HOST') + ':' + env('GRAFANA_PORT')

        headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}
        
        with open(f'node/grafana/dashboards/Hermes/default{Device.id}.json', 'w') as f:
            f.write(pretty_json)

        r = requests.post(f"http://{server}/api/admin/provisioning/dashboards/reload", auth=(env('GRAFANA_USER'), env('GRAFANA_PASSWORD')))
        print(f"{r.status_code} - {r.content}")
