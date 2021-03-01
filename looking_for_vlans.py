from netmiko import ConnectHandler
from operator import itemgetter
from getpass import getpass
import json

username = input('Enter your username: ')
password = getpass()
vlanid = input('What switches have this vlan: ')

with open('H:\Scripts\KEEPERS\devices') as f:
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

    output = net_connect.send_command('show vlan', use_textfsm=True)


    #print(json.dumps(output, indent=2))

    output1 = net_connect.send_command('show interface switchport', use_textfsm=True)

  
    for interface in output1:
        vlans = interface['trunking_vlans'][0].split(',')
        if vlanid in vlans:
            print(f"{interface['interface']} is a trunk and has vlan " + vlanid + " on it")
  






    #print(json.dumps(output1, indent=2))

    

