from netmiko import ConnectHandler
from operator import itemgetter
from getpass import getpass
import json

username = input('Enter your username: ')
password = getpass()

with open('H:\Scripts\TEXTFSM\device_file.txt') as f:
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
#This is so I can see what part are being allowed and what are being blocked 
#without manually logging in or going to the RADIUS server
#I am using more NTC Templates to get structured data
    output = net_connect.send_command('show authentication sessions', use_textfsm=True)

    print ('\nAuthorized Devices\n')
    for interface in output:
        if interface['status'] == 'Auth':
            print(f"{interface['mac']} is authorized on port {interface['interface']} and is on the {interface['domain']} domain")

    print ('\nUnauthorized Devices\n')
    for interface in output:
        if interface['status'] != 'Auth':
            print(f"{interface['mac']} is not authorized on port {interface['interface']}")

    net_connect = ConnectHandler(**SW)

    #print(json.dumps(output, indent=2))
    #results from the dump
    #"interface": "Gi1/0/10",
    #"mac": "0008.5d71.c2e8",
    #"method": "dot1x",
    #"domain": "VOICE",
    #"status": "Auth",
    #"session": "0A000C14000289E2D731909D"