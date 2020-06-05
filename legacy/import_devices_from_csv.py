import csv
from netbox_rac import NetboxConnection

file_path = 'device_import.csv'
server = 'docker1:8080'
token = '0123456789abcdef0123456789abcdef01234567'

connection = NetboxConnection(token,server)

with open(file_path,'r') as csvfile:
    device_data = csv.DictReader(csvfile)

    for row in device_data:
        row = dict(row)
        response = connection.create_device(device_name=row['name'],
            site_name=row['site'],
            device_role=row['role'],
            manufacturer_name=row['manufacturer'],
            device_type=row['type'],
            platform_name=row['platform'])
        print(response)