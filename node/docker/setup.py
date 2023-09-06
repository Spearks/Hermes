# Setup agent for Grafana
import os.path
import requests

GRAFANA_USER = os.environ.get('GRAFANA_USER', 'admin')
GRAFANA_PASSWORD = os.environ.get('GRAFANA_USER', 'password')

def setup_env()


# Check if is a Docker Env
if file('/.dockerenv'): 
    print("Im not in a Docker container")
else: 
    setup_env()