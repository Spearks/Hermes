from .views import (
    home_view, 
    devices_view,
    channel_view,
    reports_view,
    channel_export_view,
    reports_list_view,
    system_view
)

from django.urls import path

urlpatterns = [
    path('', home_view),
    path('devices', devices_view), 
    path('channel/<int:ch>', channel_view), 
    path('reports', reports_view), 
    path('reports/list', reports_list_view), 
    path('channel/excel/', channel_export_view), 
    path('system', system_view)
]