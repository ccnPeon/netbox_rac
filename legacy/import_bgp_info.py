import csv
from netbox_rac import NetboxConnection

file_path = 'bgp_info.csv'
server = 'docker1:8080'
token = '0123456789abcdef0123456789abcdef01234567'

connection = NetboxConnection(token,server)

with open(file_path,'r') as csvfile:
    bgp_data = csv.DictReader(csvfile)

    # Get BGP Information per device
    device_bgp_as_data = {}
    device_bgp_neighbors_data = {}
    for row in bgp_data:
        row = dict(row)

        # Get BGP AS Information and check for conflicts
        if row['device_name'] not in device_bgp_as_data:
            device_bgp_as_data[row['device_name']] = row['bgp_as']
        elif row['device_name'] in device_bgp_as_data and device_bgp_as_data[row['device_name']] != row['bgp_as']:
            print('Exiting due to Error: Conflicting AS found in file for device: {0}'.format(row['device_name']))
            exit()

        # Get BGP Neighbor Information
        if row['device_name'] not in device_bgp_neighbors_data:
            device_bgp_neighbors_data[row['device_name']] = {}
        
        if row['bgp_peer_name'] not in device_bgp_neighbors_data[row['device_name']]:
            device_bgp_neighbors_data[row['device_name']][row['bgp_peer_name']] = []

        device_bgp_neighbors_data[row['device_name']][row['bgp_peer_name']].append(row['bgp_neighbor_ip'])
        
    # Add BGP AS to devices
    for device_name in device_bgp_as_data:
        bgp_as = device_bgp_as_data[device_name]
        response = connection.add_device_bgp_as(device_name,bgp_as)
        print(response)

    # Add BGP Neighbors to Device
    for device_name in device_bgp_neighbors_data:
        for peer in device_bgp_neighbors_data[device_name]:
            for neighbor_ip in device_bgp_neighbors_data[device_name][peer]:
                response = connection.add_device_bgp_neighbor(device_name,neighbor_ip,peer)
                print(response)