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
        r = requests.post(f"http://{server}/api/admin/provisioning/dashboards/reload", auth=(env('GRAFANA_USER'), env('GRAFANA_PASSWORD')))
        print(f"{r.status_code} - {r.content}")

        with open(f'node/grafana/dashboards/Hermes/default{Device.id}.json', 'w') as f:
            f.write(pretty_json)
    # devices = DeviceModel.objects.all()

    # for Device in devices: 

    #     Channels = Channel.objects.all().filter(device=Device)

    #     dashboard = Dashboard(
    #         title=Device.name ,
    #         description=Device.desc,
    #         tags=[
    #             'hermes-auto-generated'
    #         ],
    #         timezone="browser",

    #         panels= [ TimeSeries(title=Channel.name, 
    #                             dataSource='default', 
    #                             targets=[Target(datasource='default', 
    #                             expr=Device.prefix + '_' + Channel.prometheus_name)],
    #                             gridPos=GridPos(h=8, w=16, x=0, y=0),
    #                             unit=Channel.unit
                                
    #                 ) 
    #                 for Channel in Channels],

    #     ).auto_panel_ids()


    #     pretty_json = json.dumps(dashboard.to_json_data(), sort_keys=True, indent=2, cls=DashboardEncoder)
    #     print("Tasks!")
    #     with open('node/grafana/dashboards/default.json', 'w') as f:
    #         f.write(pretty_json)

@app.task
def export_metric_data(time_intervals, channel, return_only_data=False):
    data_list = []

    for start_time, end_time, resolution in time_intervals:
        start_time = parse_datetime(start_time)
        end_time = parse_datetime(end_time)
        resolution = str(60 / int(resolution))
 
        metric_data = prom.get_metric_range_data(metric_name=channel, start_time=start_time, end_time=end_time)

        
        for data in MetricsList(metric_data):

            df = pd.DataFrame(data.metric_values)
            df["ds"] = pd.to_datetime(df["ds"])


            df = df.set_index("ds")

            try:
                sd = df.resample(resolution + 'S').ffill()
            except ValueError as ve:
                return {"return" : "Error","message" : "Frequência impossível", "code" : str(ve)}
            data_list.append(sd)

    try:
        final_df = pd.concat(data_list)

        if return_only_data == True:
            final_df = final_df.reset_index()
            return final_df.to_json(orient='split') 

        lines = len(final_df)
        file_name = f'export{ str(random.randint(0, 99999)) }.xlsx'
        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'exported', file_name)
        
        final_df.to_excel(temp_file_path, index=True)

        with open(temp_file_path, 'rb') as f:
            exported_data = FileExportModel()
            exported_data.lines = lines
            
            exported_data.xlsx_file.save(file_name, File(f))

        os.remove(temp_file_path)

        return {"return" : "Object", "message" : None, "code" : str(exported_data.id)}

        
    except ValueError as ve:
        
        return {"return" : "Error","message" : "Sem objetos para exportar", "code" : str(ve)}


