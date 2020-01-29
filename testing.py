import requests
import json
from netbox_rac import NetboxConnection
from pprint import pprint

server = 'docker1:8080'
model = '7280SR'
manufacturer = 'Arista'
role = 'LEAF'
# token = ''
token = '0123456789abcdef0123456789abcdef01234567'
new_devices = ['EOS2', 'EOS3', 'EOS4', 'EOS5']
site = 'OHV_LAB_SIM'


device_list = {
    # 'EOS1': {
    #     'role': 'Spine',
    #     'ip': '10.255.255.31/24'
    # },
    # 'EOS2': {
    #     'role': 'Spine',
    #     'ip': '10.255.255.32/24'
    # },
    # 'EOS3': {
    #     'role': 'Spine',
    #     'ip': '10.255.255.33/24'
    # },
    # 'EOS4': {
    #     'role': 'Spine',
    #     'ip': '10.255.255.34/24'
    # },
    'EOS5': {
        'role': 'Spine',
        'interfaces': {
            "Management1": {
                "vrf": 'MGMT',
                "ip": '10.255.255.35'
            }
        }
    },
    

}

connection = NetboxConnection(token,server)


# for device in device_list:
#     response = connection.create_device(device, site, device_list[device]['role'], manufacturer, model,primary_ipv4=device_list[device]['ip']) 
#     print(response)


# ips = connection.get_ip_address_all()
# print(ips)

# ip = connection.get_ip_address_specific('10.255.255.31')
# print(ip)

# manufacturer_data = connection.get_manufacturer_by_name(manufacturer)
# print(manufacturer_data)

# device_type_data = connection.get_device_type(model)
# print(device_type_data)

# device_role = connection.get_device_role(role)
# print(device_role)

# new_device = connection.create_device('EOS2', site, role, manufacturer, model)
# print(new_device)

# device = connection.get_device_by_name('EOS5')
# pprint(device)

# interface = connection.get_interface_by_id(1)
# pprint(interface)

# ip = connection.get_ip_address_specific('10.255.255.35/24')
# pprint(ip)

ip = connection.add_ip_address('10.255.255.37/24', 'MGMT')
pprint(ip)

ip = connection.add_ip_address_to_interface('10.255.255.37/24', 'EOS5', 'Ethernet2', 'eos5.greer.net')
pprint(ip)

# interface = connection.get_interface_all()
# print(interface)

# new_interface = connection.add_interface_to_device('EOS5', 'Ethernet2', {'ipv4': '10.255.255.35', 'type': '10gbase-x-sfpp'})
# print(new_interface)

# devices = connection.get_device_by_id(1)
# print(devices)

# site = connection.create_site(site)
# print(site)


# for device in devices:
#     print(device['name'])

# for new_device in new_devices:
#     device_id = str(new_id)
#     new_device_payload = {"id": new_id, "name": new_device, "site": site_data, ""}
#     print(new_device_payload)

# new_device_post = json.loads(requests.post(url=url+'/{0}'.format(new_id),))
