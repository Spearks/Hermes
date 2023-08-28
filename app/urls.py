from .views import (
    home_view, 
    devices_view,
    devices_list_view,
    channel_view,
    reports_view,
    channel_export_endpoint,
    channel_export_view,
    channel_list_device,
    channels_view_by_device,
    reports_list_view,
    system_view,
    multiple_channels_export_view,
    sheet_preview, 
    server_state,
    admin_settings_view
)

from django.urls import path

urlpatterns = [
    path('', home_view),
    path('view/<int:device>', devices_view), 
    path('devices/', devices_list_view),
    path('channel/<int:ch>', channel_view), 
    path('reports', reports_view), 
    path('reports/list', reports_list_view), 
    path('channel/export/view/<int:ch>', channel_export_view),
    path('channel/export/view/multiple/', multiple_channels_export_view),
    path('channel/list/device/<int:device>', channel_list_device),
    path('channel/list/view/byDevice/<int:device>', channels_view_by_device),
    path('channel/export/file/xlsx', channel_export_endpoint), 
    path('settings', admin_settings_view),
    path('reports/preview', sheet_preview),
    path('api/v1/server/state', server_state),
    path('system', system_view),
]