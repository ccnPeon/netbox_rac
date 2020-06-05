import requests
import json
from netbox_rac import NetboxConnection
from pprint import pprint

server = 'docker1:8080'
token = '0123456789abcdef0123456789abcdef01234567'

api_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token {0}'.format(token),
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'cache-control': 'no-cache'
}

url = 'http://{0}/api/dcim/devices/46/napalm/?method=get_environment'.format(server)

response = requests.get(url,headers=api_headers,verify=False)
print(response.content)