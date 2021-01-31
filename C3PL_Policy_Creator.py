from netmiko import ConnectHandler
from getpass import getpass
from ntc_templates.parse import parse_output
from jinja2 import Environment, FileSystemLoader
import json


#Through the power of NTC-Templates and Jinja2 templates I put together a 
#script here that will log into switches on the device_file.txt and do a show vlan
#and that all vlans that are active and minus the default vlan are pulled
#and used in the policy template to give me a nice config that I can just upload
#to my switches.

file_loader = FileSystemLoader('Z:\Scripts\Python2')

env = Environment(loader=file_loader)
template = env.get_template('policy.j2')

username = input('Enter your username: ')
password = getpass()

with open('Z:\Scripts\Python2\device_file.txt') as f:
    devices_list = f.read().splitlines()

for devices in devices_list:
    print ('Connecting to device" ' + devices)
    ip_address_of_device = devices
    SW = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device, 
        'username': username,
        'password': password
    }

    net_connect = ConnectHandler(**SW)

vlans = (net_connect.send_command("show vlan", use_textfsm=True))

for vlan in vlans:
    if vlan['status'] == 'active' and vlan['name'] != 'default':
        vlans = (vlan['vlan_id'],)
        
        file = open('Z:\Scripts\Python2\Policy' +ip_address_of_device,'a')

    
        output = template.render(vlans=vlans)

        print(output)
        file.write(output)
        file.close()

