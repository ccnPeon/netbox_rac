import json
import requests
import yaml
import ast

class NetboxConnection():
    def __init__(self,token,server):
        self.api_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token {0}'.format(token),
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'cache-control': 'no-cache'
        }
        self.api_root ='http://{0}/api'.format(server)


    ##### Site API Calls #####
    def get_all_sites(self):
        '''
        Get site data for the given for all sites
        
        args:
            None
        
        return:
            site_data: list[dict]
        '''
        url = self.api_root+'/dcim/sites/'
        site_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results']
        return site_data

    def get_site_by_name(self,site_name):
        '''
        Get site data for the given site name.
        
        args:
            site_name: string
        
        return:
            site_data: dict
        '''
        url = self.api_root+'/dcim/sites/?name={0}'.format(site_name)
        site_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results'][0]
        if site_data:
            return site_data

    
    def get_site_by_id(self,site_id):
        '''
        Get site data for the given site id.
        
        args:
            site_id: integer
        
        return:
            site_data: dict
        '''
        url = self.api_root+'/dcim/sites/{0}/'.format(site_id)
        site_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)
        if site_data and 'detail' not in site_data:
            return site_data
        elif 'detail' in site_data and site_data['detail'] == 'Not found.':
            print("Site id not found.")
            exit()
    
    def create_site(self,site_name,facility='',slug='',description=''):
        '''
        Creates a new site with the given name.
        
        args:
            *required*
            site_name: string

            *optional*
            facility: string
            slug: string
            description: string
        
        return:
            site_creation_result: dict
        '''
        #API call to create site
        url = self.api_root+'/dcim/sites/'
        site_payload = {
            "name": site_name,
            "facility": facility,
            "slug": slug if slug != '' else site_name.lower(),
            "description": description,
            }
            
        site_creation_result = json.loads(requests.post(url=url, headers=self.api_headers, data=json.dumps(site_payload), verify=False).content)

        if 'already exists' in site_creation_result['name'][0]:
            print("Site with this name already exists. Please choose a different name.")
            exit()
        elif 'already exists' in site_creation_result['slug'][0]:
            print("Site with this slug already exists. Please choose a different slug.")
            exit()
        else:
            print('Site {0} successfully created with id: {1}'.format(site_name,site_creation_result['id']))
            return(site_creation_result)


    ##### Device API Calls #####
    def get_all_devices(self):
        '''
        Get device data for all devices
        
        args:
            None
        
        return:
            device_data: list[dict]
        '''
        url = self.api_root+'/dcim/devices/'
        device_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results']
        return device_data

    def get_device_by_name(self,device_name):
        '''
        Get device data for the given device name.
        
        args:
            device_name: string
        
        return:
            device_data: dict
        '''
        url = self.api_root+'/dcim/devices/?name={0}'.format(device_name)
        device_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results'][0]
        if device_data:
            return device_data

    
    def get_device_by_id(self,device_id):
        '''
        Get device data for the given device id.
        
        args:
            device_id: integer
        
        return:
            device_data: dict
        '''
        url = self.api_root+'/dcim/devices/{0}/'.format(device_id)
        device_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)
        if device_data and 'detail' not in device_data:
            return device_data
        elif 'detail' in device_data and device_data['detail'] == 'Not found.':
            print("Device ID not found.")
            exit()

    def get_device_type(self,device_type):
        '''
        Get device type information for given device type.
        
        args:
            device_type: string
        
        return:
            device_type_data: dict
        '''
        url = self.api_root+'/dcim/device-types/?model={0}'.format(device_type)
        device_type_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results'][0]
        return device_type_data

    def get_device_role(self,device_role):
        '''
        Get device role information for given device role.
        
        args:
            device_role: string
        
        return:
            device_role_data: dict
        '''
        url = self.api_root+'/dcim/device-roles/?name={0}'.format(device_role)
        device_role_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results'][0]
        return device_role_data

    def get_devices_by_site(self,site_name):
        '''
        Gets device information for all devices in a site
        
        args:
            site_name: string
        
        return:
            device_data: dict
        '''
        url = self.api_root+'/dcim/devices/?site={0}'.format(site_name.lower())
        device_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results']
        return device_data


    def create_device(self,device_name,site_name,device_role,manufacturer_name,device_type,platform_name='',serial_number='',asset_tag=None,status=1):
        '''
        Creates a new device with the given name.
        
        args:
            *required*
            device_name: string
            site_name: string
            device_role: string
            manufacturer_name: string
            device_type: string

            *optional*
            serial_number: string
            asset_tag: string
            status: int
            platform_name: string
        
        return:
            device_creation_result: dict
        '''

        #API call to create site
        url = self.api_root+'/dcim/devices/'

        device_payload = json.dumps({
            "name": device_name,
            "site": self.get_site_by_name(site_name)['id'],
            "manufacturer": self.get_manufacturer_by_name(manufacturer_name)['id'],
            "device_role": self.get_device_role(device_role)['id'],
            "device_type": self.get_device_type(device_type)['id'],
            "platform": self.get_platform_by_name(platform_name)['id'],
            "serial": serial_number,
            "asset_tag": asset_tag,
            "status": status
            })

        for device in self.get_all_devices():
            if device['name'] == device_name:
                print("Device with this name ({0}) already exists. Please choose a different name.".format(device_name))
                return None
            elif device['serial'] != '' and device['serial'] == serial_number:
                print("Device with this serial number ({0}) already exists. Please choose a different name.".format(serial_number))
                return None
            elif device['asset_tag'] and device['asset_tag'] == asset_tag:
                print("Device with this asset tag ({0}) already exists. Please choose a different name.".format(asset_tag))
                return None

        device_creation_result = json.loads(requests.post(url=url, headers=self.api_headers, data=device_payload, verify=False).content)
        return(device_creation_result)

    def get_device_bgp_as(self,device_name):
        '''
        Get BGP AS for given device

        args:
            device_name: string
        
        return:
            bgp_as: integer
        '''
        return self.get_device_by_name(device_name)['custom_fields']['bgp_as']

    def get_device_bgp_neighbors(self,device_name):
        '''
        Get BGP AS for given device

        args:
            device_name: string
        
        return:
            bgp_neighbors: list(dict)
        '''
        return self.get_device_by_name(device_name)['custom_fields']['bgp_neighbors']

    def add_device_bgp_as(self,device_name,bgp_as):
        '''
        Adds BGP AS to device if a BGP AS does not already exist.

        args:
            device_name: string
            bgp_as: integer
        
        return:
            bgp_as_addition_result: dict
        '''
        temp_device_data = self.get_device_by_name(device_name)
        if temp_device_data['custom_fields']['bgp_as'] != None:
            print('Device {0} already has BGP AS of {1}.'.format(device_name,temp_device_data['custom_fields']['bgp_as']))
            print('If you want to update the BGP AS, please use "update_device_bgp_as" method instead.')
            return None
        url = self.api_root+'/dcim/devices/{0}/'.format(temp_device_data['id'])
        bgp_as_addition_payload = json.dumps({
            "site": temp_device_data['site']['id'],
            "device_type": temp_device_data['device_type']['id'],
            "device_role": temp_device_data['device_role']['id'],
            "custom_fields": {
                "bgp_as": bgp_as,
            },
        })
        bgp_as_addition_result = json.loads(requests.put(url=url, headers=self.api_headers,
                                                         data=bgp_as_addition_payload,
                                                         verify=False).content)
        return bgp_as_addition_result

    def add_device_bgp_neighbor(self,device_name,bgp_neighbor_ip,bgp_peer_name):
        '''
        Adds BGP Neighbor to device.

        args:
            device_name: string
            bgp_neighbor_ip: string
            bgp_peer_name: string
        
        return:
            bgp_neighbor_addition_result: dict
        '''
        print('***** DEBUG DEVICE {0}****'.format(device_name))
        temp_device_data = self.get_device_by_name(device_name)
        bgp_peer_as = self.get_device_bgp_as(bgp_peer_name)
        if bgp_peer_as == None:
            print("No Peer AS Found.")
            return None
        elif temp_device_data['custom_fields']['bgp_as'] == None:
            print("Neighbor cannot be created on {0} because it does not have a BGP AS assigned.".format(device_name))
            return None
        url = self.api_root+'/dcim/devices/{0}/'.format(temp_device_data['id'])
        if temp_device_data['comments']:
            comments = ast.literal_eval(temp_device_data['comments'])
        else:
            comments = {}
        if 'bgp_neighbors' not in comments or comments['bgp_neighbors'] == None:
            current_neighbors = []
        else:
            current_neighbors = comments['bgp_neighbors']
            for neighbor in current_neighbors:
                if neighbor['bgp_neighbor_ip'] == bgp_neighbor_ip:
                    print('Skipping Neighbor IP: Neighbor {0} IP {1} already present for device: {2}'.format(bgp_peer_name,bgp_neighbor_ip,device_name))
                    return None
        current_neighbors.append({"bgp_neighbor_ip": bgp_neighbor_ip, "bgp_peer_as": bgp_peer_as, "bgp_peer_description": bgp_peer_name})
        bgp_neighbor_addition_payload = json.dumps({
            "site": temp_device_data['site']['id'],
            "device_type": temp_device_data['device_type']['id'],
            "device_role": temp_device_data['device_role']['id'],
            "comments": str({
                "bgp_neighbors": current_neighbors,
            }),
        })
        bgp_neighbor_addition_result = requests.put(url=url, headers=self.api_headers,
                                                         data=bgp_neighbor_addition_payload,
                                                         verify=False).content
        return bgp_neighbor_addition_result

    def get_device_bgp_neighbors(self,device_name):
        '''
        Gets BGP Neighbors for given device.

        args:
            device_name: string
        
        return:
            bgp_neighbors: dict
        '''
        device_data = self.get_device_by_name(device_name)
        if device_data['comments']:
            comments = ast.literal_eval(device_data['comments'])
        else:
            return []
        if 'bgp_neighbors' not in comments or comments['bgp_neighbors'] == None:
            return []
        else:
            return comments['bgp_neighbors']
    
    def update_device_bgp_as(self,device_name,bgp_as):
        '''
        Updates BGP AS on given device.

        args:
            device_name: string
            bgp_as: integer
        
        return:
            bgp_as_update_result: dict
        '''
        temp_device_data = self.get_device_by_name(device_name)
        url = self.api_root+'/dcim/devices/{0}/'.format(temp_device_data['id'])
        bgp_as_update_payload = json.dumps({
            "site": temp_device_data['site']['id'],
            "device_type": temp_device_data['device_type']['id'],
            "device_role": temp_device_data['device_role']['id'],
            "custom_fields": {
                "bgp_as": bgp_as,
            },
        })
        bgp_as_update_result = json.loads(requests.put(url=url, headers=self.api_headers,
                                                         data=bgp_as_update_payload,
                                                         verify=False).content)
        return bgp_as_update_result


    ##### Manufacturer API Calls #####
    def get_manufacturer_by_name(self,manufacturer_name):
        '''
        Get manufacturer data for the given manufacturer name.
        
        args:
            manufacturer_name: string
        
        return:
            manufacturer_data: dict
        '''
        url = self.api_root+'/dcim/manufacturers/?name={0}'.format(manufacturer_name)
        manufacturer_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results'][0]
        return manufacturer_data

    def create_manufacturer(self,manufacturer_name):
        '''
        Creates manufacturer with given name.

        args:
            manufacturer_name: string

        return:
            dict
        '''
        payload = json.dumps({
            'name': manufacturer_name,
            'slug': manufacturer_name.lower()

        })
        url = self.api_root+'/dcim/manufacturers/'
        response = json.loads(requests.post(url=url, headers=self.api_headers, verify=False).content)
        return response

    ##### Platform API Calls #####
    def get_platform_by_name(self,platform_name):
        '''
        Gets platform information for given platform name

        args:
            platform_name: string
        
        return:
            platform_data: dict
        '''
        url = self.api_root+'/dcim/platforms/?name={0}'.format(platform_name)
        platform_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results'][0]
        return platform_data

    ##### IPAM API Calls #####

    def get_vrf_by_name(self,vrf_name):
        '''
        Gets vrf information for given vrf name

        args:
            vrf_name: string
        
        return:
            vrf_data: dict
        '''
        url = self.api_root+'/ipam/vrfs/?name={0}'.format(vrf_name)
        vrf_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results'][0]
        return vrf_data

    def get_ip_address_all(self):
        '''
        Gets all ip addresses

        args:
            none
        
        return:
            ip_data: dict
        '''
        url = self.api_root+'/ipam/ip-addresses'
        ip_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results']
        return ip_data

    def get_ip_address_specific(self,ip_address):
        '''
        Gets ip information for given ip address.

        args:
            ip_address: string
        
        return:
            ip_data: dict
        '''
        url = self.api_root+'/ipam/ip-addresses/?address={0}'.format(ip_address)
        ip_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results'][0]
        return ip_data

    def add_ip_address(self,ip_address,vrf_name,nat_outside=None):
        '''
        Adds IP address information.

        args:
            *required*
            ip_address: string
            vrf_name: string

            *optional*
            nat_outside: string

        return:
            ip_creation_result: dict
        '''
        url = self.api_root+'/ipam/ip-addresses/'
        ip_payload = json.dumps({
            "address": ip_address,
            "vrf": self.get_vrf_by_name(vrf_name)['id'],
            "nat_outside": nat_outside
        })
        ip_creation_result = json.loads(requests.post(url=url, headers=self.api_headers, data=ip_payload, verify=False).content)
        return ip_creation_result
    
    def add_ip_address_to_interface(self,ip_address,device_name,interface,fqdn=''):
        '''
        Adds IP addfress to device interface.

        args:
            *required*
            ip_address: string
            device_name: string
            interface: string

            *optional*
            fqdn: string

        return:
            ip_addition_result: dict
        '''
        interface_list = self.get_interface_all()
        interface_id = 0
        device_id = 0
        for interface_item in interface_list:
            if interface_item['name'] == interface and interface_item['device']['name'] == device_name:
                interface_id = interface_item['id']
                device_id = interface_item['device']['id']

        temp_ip_data = self.get_ip_address_specific(ip_address)
        url = self.api_root+'/ipam/ip-addresses/{0}/'.format(temp_ip_data['id'])
        temp_ip_data = self.get_ip_address_specific(ip_address)
        ip_addition_payload = {
            "address": ip_address,
            "status": temp_ip_data['status']['value'],
            "vrf": temp_ip_data['vrf']['id'],
            "dns_name": fqdn.lower(),
            "interface": interface_id,
            "description": temp_ip_data['description'],
            "nat_outside": temp_ip_data['nat_outside'],
        }
        if temp_ip_data['tenant']:
            ip_addition_payload['tenant'] = temp_ip_data['tenant']['id']
        if temp_ip_data['nat_inside']:
            ip_addition_payload['nat_inside'] = temp_ip_data['nat_inside']
        if temp_ip_data['role']:
            ip_addition_payload['role'] = temp_ip_data['role']

        ip_addition_payload = json.dumps(ip_addition_payload)
        ip_addition_result = requests.put(url=url, headers=self.api_headers, data=ip_addition_payload, verify=False).content

        return ip_addition_result

    def assign_primary_ip_to_device(self,device_name,ip_address):
        '''
        Adds IP address as primary IP for a given device

        args:

            device_name: string
            ip_address: string


        return:
            primary_ip_addition_result: dict
        '''
        temp_device_data = self.get_device_by_name(device_name)
        url = self.api_root+'/dcim/devices/{0}/'.format(temp_device_data['id'])
        temp_ip_data = self.get_ip_address_specific(ip_address)
        primary_ip_addition_payload = json.dumps({
            "site": temp_device_data['site']['id'],
            "device_type": temp_device_data['device_type']['id'],
            "device_role": temp_device_data['device_role']['id'],
            "primary_ip4": temp_ip_data['id'],
            "primary_ip": ip_address
        })
        primary_ip_addition_result = json.loads(requests.put(url=url, headers=self.api_headers,
                                                         data=primary_ip_addition_payload,
                                                         verify=False).content)
        return primary_ip_addition_result



    ##### Interface API Calls #####
    def get_interface_all(self):
        '''
        Gets all interfaces

        args:
            none

        return:
            interface_data: dict
        '''
        url = self.api_root+'/dcim/interfaces'
        interface_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)['results']
        return interface_data

    def get_interface_by_id(self,interface_id):
        '''
        Gets interface for given interface id

        args:
            interface_id: int

        return:
            interface_data: dict
        '''
        url = self.api_root+'/dcim/interfaces/{0}'.format(interface_id)
        interface_data = json.loads(requests.get(url=url, headers=self.api_headers, verify=False).content)
        return interface_data

    def add_interface_to_device(self,device_name,interface_name,interface_type,mtu=1500):
        '''
        Adds interface to given device

        args:
            *required*
            device_name: string
            interface_name: string
            interface_type: string
            
            *optional*
            mtu: int

        return:
            interface_creation_result: dict
        '''
        url = self.api_root+'/dcim/interfaces/'
        interface_payload = json.dumps({
            "name": interface_name,
            "device": self.get_device_by_name(device_name)['id'],
            "type": interface_type,
            "mtu": mtu
        })
        interface_creation_result = json.loads(requests.post(url=url, headers=self.api_headers, data=interface_payload, verify=False).content)
        return interface_creation_result
