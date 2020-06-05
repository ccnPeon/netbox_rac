from build.tools.netbox_rac import NetboxConnection
import jinja2
from pprint import pprint

server = 'docker1:8080'
token = '0123456789abcdef0123456789abcdef01234567'
target_site = 'OHV_LAB_SIM'

def render_config_template(hostvars, template):
    with open(template, 'r') as file:
        template = file.read()
    env = jinja2.Environment(
        loader=jinja2.BaseLoader(),
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=['jinja2.ext.do'])
    templategen = env.from_string(template)
    if templategen:
        config = templategen.render(hostvars)
        return(config)
    return(None)

connection = NetboxConnection(token,server)

target_devices = connection.get_devices_by_site(target_site)

for device in target_devices:
    if device['name'] == 'EOS1': # remove when done with testing
        device_name = device['name']
        # Get all device information
        device_interfaces = [ interface for interface in connection.get_interfaces_for_device(device['name']) ]
        device_ips = [ip for ip in connection.get_ip_addresses_for_device(device['name'])]

        host_vars = {
            "device_name": device_name,
            "device_interfaces": device_interfaces,
            "device_ips": device_ips
        }

        # #### Begin configuration generation
        device_configuration = "enable \nconfigure terminal\n"

        # # Interface Configuration
        device_configuration += render_config_template(host_vars, './jinja/interfaces/interfaces.j2') + '\n'

        print(device_configuration)
