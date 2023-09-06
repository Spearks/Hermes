import requests
# Caminho do Grafana
url = 'http://localhost:3000/api/admin/users/admin/password'
# Senha de administrador (que deve ser mudada)
username = 'admin'
password = 'admin'

payload = {
    'password' : 'olamundo'
}

response = requests.post(url, json=payload, auth=(username, password))
if response.status_code == 200:
    token_data = response.json()
    print(token_data)
else:
    print('Erro:', response.text)