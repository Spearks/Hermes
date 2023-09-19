from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ExportMultipleChannelsSerializer, Export
from app.tasks import export_metric_data
from prometheus_api_client.utils import parse_datetime
from app.models import Channel, FileExportModel
import pandas as pd
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.management import call_command
import io
from django.core.files.base import ContentFile
# Create your views here.

def convert_to_export_objects(data_list):
    export_objects = []
    for item in data_list:
        export_object = Export(
            time=item['time'],
            endtime=item['endtime'],
            pmin=item['pmin'],
            channelId=item['channelId']
        )
        export_objects.append(export_object)
    return export_objects


class ExportChannelsView(viewsets.ViewSet):
    def create(self, request):
        serializer = ExportMultipleChannelsSerializer(data=convert_to_export_objects(request.data), many=True)
        data_list = []

        # Check if the object recived is correct
        try:
            serializer.is_valid()
            ExportMultipleChannelsSerializer.validate(serializer)
        except Exception: 
            return Response("Error! Validação", status=status.HTTP_400_BAD_REQUEST)

        dataByChannel = {}  
        excel_bytesio = io.BytesIO()
        excel_writer = pd.ExcelWriter(excel_bytesio, engine='xlsxwriter')
        workbook = excel_writer.book


        for Export in serializer.data:
            chid = int(Export['channelId'])
            dataByChannel[chid] = []

        for Export in serializer.data:
            #if dataByChannel[Export['channelId']] == None: dataByChannel[Export['channelId']] = []

            interval = (parse_datetime(Export['time']), parse_datetime(Export['endtime']), int(Export['pmin']))
            
            channel = Channel.objects.get(pk=Export['channelId'])
            ex = channel.device.prefix + '_' + channel.prometheus_name
            
            data = export_metric_data.delay(time_intervals=[interval], channel=ex, return_only_data=True).get()
            
           
            # Check if the variable is a dict, because Errors are returned in a dict format.
            if isinstance(data, dict):
                return Response({"error" : data})
            
            # Transform the json_data to a dataframe.
            data_dict = json.loads(data)
            #columns = pd.MultiIndex.from_tuples(data_dict['columns'])
            data = data_dict['data']
        
            df = pd.DataFrame(data, columns=['ds', 'y'])

            df['ds'] = pd.to_datetime(df['ds'], unit='ms')
            df['ds'] = df['ds'].dt.strftime('%Y-%m-%d %H:%M:%S')

            ch = str(Export['channelId'])
            
            df = df.rename(columns={'ds': 'Tempo', 'y': 'Valor'})

            # Write the DataFrame to the Excel sheet
            df.to_excel(excel_writer, sheet_name=f'Canal {ch}', startrow=1, header=False, index=False)
            
            # Get the worksheet object to add column headers
            worksheet = excel_writer.sheets[f'Canal {ch}']
            header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#D7E4BC', 'border': 1})
            for col_num, column_name in enumerate(df.columns):
                worksheet.write(0, col_num, column_name, header_format)
        
        excel_writer.close()
        
        excel_bytesio.seek(0)
        file_export = FileExportModel()
        file_export.xlsx_file.save('multiexport.xlsx', ContentFile(excel_bytesio.getvalue()))
        file_export.lines = 0  
        file_export.save()

        return Response({"message": "Data received and processed successfully", "object" : file_export.filename()}, status=status.HTTP_201_CREATED)
        
class SystemActionsView(viewsets.ViewSet):

    def create(self, request):

        action = request.data.get('action')

        if action == 'reload_grafana':
            return Response({'message': 'Action reload_grafana executed'}, status=status.HTTP_200_OK)

