from hermes.celery import app
import requests
from hermes.settings import env
from app.models import Channel, DeviceModel

GRAFANA_API_TOKEN=env('GRAFANA_TOKEN').rstrip()
GRAFANA_HOST=env('GRAFANA_HOST').rstrip()
GRAFANA_PORT=str(env('GRAFANA_PORT')).rstrip()
GRAFANA_API_URL=f"http://{GRAFANA_HOST}:{GRAFANA_PORT}"


@app.task
def get_dashboards_by_name_and_tag(name, tag):
    url = f'{GRAFANA_API_URL}/api/search?type=dash-db&query={name}'

    headers = {
        'Authorization': f'Bearer {GRAFANA_API_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dashboards = response.json()
        filtered_dashboards = [dashboard for dashboard in dashboards if tag in dashboard.get('tags', []) if dashboard.get('title') == name ]
        return filtered_dashboards
    else:
        raise Exception(f'Failed to retrieve dashboards: {response.text}')


@app.task
def get_panels_by_uid(uid):

    url = f'{GRAFANA_API_URL}/api/dashboards/uid/{uid}'
    headers = {
        'Authorization': f'Bearer {GRAFANA_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers).json()
    
    dashboard_data = response 
    panels = dashboard_data['dashboard']['rows']
    
    return panels

@app.task
def return_panels_view(panels, device):
    results = {}
    device_expr = DeviceModel.objects.get(id=device).prefix

    list_expr = [ device_expr + '_' + channel.prometheus_name for channel in Channel.objects.all().filter(device=device)]

    # create empty dict
    for expr in list_expr:
        results[expr] = {'avg': None, 'max': None, 'min': None, 'default' : None}

    for panel in panels[0]["panels"]:
        panel_expr = panel["targets"][0]["expr"]
    
        for expr in list_expr:
            
            if expr in panel_expr:
                
                # identify the type of expr
                if panel_expr.startswith('avg'):
                    results[expr]['avg'] = [ panel_expr, panel["id"]]
                elif panel_expr.startswith('max'):
                    results[expr]['max'] = [ panel_expr, panel["id"]]
                elif panel_expr.startswith('min'):
                    results[expr]['min'] = [ panel_expr, panel["id"]]
                elif panel_expr == expr:
                    results[expr]['default'] = [ expr, panel["id"]]

    return results
