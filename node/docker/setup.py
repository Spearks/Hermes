import os.path
import requests
from os.path import exists
import time

class TokenCreationError(Exception):
    pass

def setup_env():
    psswd = os.getenv('GRAFANA_PASSWORD', 'password').rstrip()

    if psswd == "admin":
        print("Warning: The password should not be the default one.")
    host = os.getenv('GRAFANA_HOST', 'grafana').rstrip()
    port = os.getenv('GRAFANA_PORT', '3000').rstrip()

    url = "http://" + host + ":" + port + "/api/auth/keys"

    username = 'admin'

    payload = {
        'name': 'Admin Token',
        'role': 'Admin',
        'permissions': [
            'provisioning:reload',
            'apikeys:create'
        ]
    }

    response = requests.post(url, json=payload, auth=(username, psswd))
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data['key']
        print('Token was created!')

        with open('.env', 'a') as f:
            f.write(f"\nGRAFANA_TOKEN={token}")
        
        os.environ["GRAFANA_TOKEN"] = token
    else:
        raise TokenCreationError(f'Error: {response.text}')

# Check if is a Docker Env
if not exists('/.dockerenv'): 
    print("I'm not in a Docker container!")
else: 
    setup_env()

