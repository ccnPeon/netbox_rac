import yaml
import json
import os
from tools.netbox_rac import NetboxConnection

server = 'docker1:8080'
token = '0123456789abcdef0123456789abcdef01234567'
connection = NetboxConnection(token,server)

# Build Environment
with open('./vars/environment_info.yaml', 'r') as yamlfile:
    build_data = yaml.safe_load(yamlfile.read())

    # Build Manufacturers
    for manufacturer in build_data['manufacturers']:
        print(connection.create_manufacturer(manufacturer))

    # Build Platforms
    for platform in build_data['platforms']:
        print(connection.create_platform(platform,build_data['platforms'][platform]['manufacturer'],
            build_data['platforms'][platform]['napalm_driver'],build_data['platforms'][platform]['napalm_arguments']))

    # Build Device Types
    for device_type in build_data['device_types']:
        print(connection.create_device_type(device_type,
            build_data['device_types'][device_type]['manufacturer'],
            build_data['device_types'][device_type]['part_number'],
            build_data['device_types'][device_type]['u_height'],
            build_data['device_types'][device_type]['is_full_depth']))

    # Build Device Roles
    for role in build_data['device_roles']:
        print(connection.create_device_role(role,build_data['device_roles'][role]['color']))


# Build Sites
for site_yaml in os.listdir('./vars/sites'):
    site_name = site_yaml.replace('.yaml', '')
    
    with open('./vars/sites/{0}'.format(site_yaml), 'r') as yamlfile:
        device_data = yaml.safe_load(yamlfile.read())

        # Build Sites
        for site in device_data['sites']:
            print(connection.create_site(site_name=site,description=device_data['sites'][site]['description']))

            # Build Devices
            for device in device_data['sites'][site]['devices']:
                device_info = device_data['sites'][site]['devices'][device]
                print(connection.create_device(device_name=device,
                    device_role=device_info['device_role'],site_name=site,
                    manufacturer_name=device_info['manufacturer'],
                    device_type=device_info['device_type'],
                    platform_name=device_info['device_platform'],
                    is_mlagged=True if 'mlag' in device_info else False,
                    mlag_interfaces=device_info['mlag']['interfaces'] if 'mlag' in device_info else '',
                    mlag_side=device_info['mlag']['side'] if 'mlag' in device_info else '',
                    bgp_as=device_info['bgp']['as'] if 'bgp' in device_info else ''))
                
                # # Build Management Interfaces for Device
                print(connection.add_interface_to_device(device_name=device,
                        interface_name='Management1',
                        interface_type='1000base-t'))

                # # Add Management IP for Device to Netbox
                print(connection.add_ip_address(ip_address=device_info['mgmt_ip'],
                    vrf_name=device_info['mgmt_vrf']))

                # # Add Management IP to Management Interface
                print(connection.add_ip_address_to_interface(ip_address=device_info['mgmt_ip'],
                    device_name=device, interface='Management1', fqdn=device_info['fqdn']))

                # # Assign Management Interface as Primary Device IP
                print(connection.assign_primary_ip_to_device(device_name=device,
                    ip_address=device_info['mgmt_ip']))

                # # Build Device Interfaces
                interface_info = device_info['interfaces']
                
                # # Create Interface
                for interface in interface_info:
                    print(connection.add_interface_to_device(device_name=device,
                        interface_name=interface,
                        interface_type=interface_info[interface]['int_type'],
                        mtu=interface_info[interface]['mtu']))
                    
                #     # Add IP Address to Netbox
                    print(connection.add_ip_address(ip_address=interface_info[interface]['ipv4'],
                        vrf_name=interface_info[interface]['vrf']))

                #     # Add IP Address to Device Interface
                    print(connection.add_ip_address_to_interface(ip_address=interface_info[interface]['ipv4'],
                        device_name=device, interface=interface, fqdn=device_info['fqdn']))

                # Add BGP Neighbors to device
                if 'bgp' in device_info:
                    # IPv4-Unicast Neighbors
                    if 'neighbors' in device_info['bgp'] and 'ipv4_unicast' in device_info['bgp']['neighbors']:
                        for neighbor in device_info['bgp']['neighbors']['ipv4_unicast']:
                            neighbor_info = device_info['bgp']['neighbors']['ipv4_unicast'][neighbor]
                            connection.add_device_bgp_neighbor(device_name=device,bgp_neighbor_ip=neighbor,
                                remote_as=neighbor_info['remote_as'], neighbor_type='ipv4_unicast',
                                description=neighbor_info['description'] if 'description' in neighbor_info else '') 
                    # EVPN Neighbors
                    if 'neighbors' in device_info['bgp'] and 'evpn' in device_info['bgp']['neighbors']:
                        for neighbor in device_info['bgp']['neighbors']['evpn']:
                            neighbor_info = device_info['bgp']['neighbors']['evpn'][neighbor]
                            connection.add_device_bgp_neighbor(device_name=device,bgp_neighbor_ip=neighbor,
                                remote_as=neighbor_info['remote_as'], neighbor_type='evpn',
                                description=neighbor_info['description'] if 'description' in neighbor_info else '') 