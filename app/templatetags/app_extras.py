from django import template
from app.models import DeviceModel

from app.grafana.tasks import (
    get_dashboards_by_name_and_tag,
    get_panels_by_uid,
    return_panels_view
)

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.simple_tag
def mount_view_by_device(device):
    Device = DeviceModel.objects.get(id=int(device))

    name = Device.name
    tag = 'hermes-auto-generated'

    filtred_dasboard = get_dashboards_by_name_and_tag.delay(name, tag).get()

    dashboard_data = get_panels_by_uid.delay(filtred_dasboard[0]['uid']).get()

    mount = return_panels_view.delay(dashboard_data, Device.id).get()

    return mount, filtred_dasboard[0]['uid']
    
@register.filter
def index(indexable, i):
    return indexable[i]
