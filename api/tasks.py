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

prom = PrometheusConnect(url =f"http://{env('PROMETHEUS_HOST')}:{env('PROMETHEUS_PORT')}", disable_ssl=True)

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
