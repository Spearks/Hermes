from django.core.management.base import BaseCommand, CommandError
from hermes.settings import env
import requests

GRAFANA_API_TOKEN=env('GRAFANA_TOKEN')
GRAFANA_HOST=env('GRAFANA_HOST')
GRAFANA_PORT=str(env('GRAFANA_PORT'))
GRAFANA_API_URL=f"http://{GRAFANA_HOST}:{GRAFANA_PORT}"

class Command(BaseCommand):
    help = "Reloads the Grafana instance"

    def handle(self, *args, **options):

        url = f'{GRAFANA_API_URL}/api/admin/provisioning/dashboards/reload'

        headers = {
            'Authorization': f'Bearer {GRAFANA_API_TOKEN}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers)

        print(response.text)

        self.stdout.write(
                self.style.SUCCESS('Successfully reloaded the Grafana instance')
        )