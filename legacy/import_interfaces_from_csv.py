import csv

from netbox_rac import NetboxConnection

file_path = 'interface_import.csv'
server = 'docker1:8080'
token = '0123456789abcdef0123456789abcdef01234567'

connection = NetboxConnection(token,server)

with open(file_path,'r') as csvfile:
    interface_data = csv.DictReader(csvfile)

    for row in interface_data:
        row = dict(row)
        response = connection.add_ip_address(ip_address=row['ipaddress'],vrf_name=row['vrf'])
        print(response)

        response = connection.add_interface_to_device(device_name=row['devicename'],
            interface_name=row['interfacename'],
            interface_type=row['interfacetype'],
            mtu=row['mtu'])
        print(response)

        response = connection.add_ip_address_to_interface(ip_address=row['ipaddress'],
            device_name=row['devicename'],
            interface=row['interfacename'],
            fqdn=row['fqdn'])
        print(response)

        if row['is_primary']:
            response = connection.assign_primary_ip_to_device(row['devicename'],row['ipaddress'])
            print(response)
