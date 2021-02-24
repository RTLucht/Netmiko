from netmiko import ConnectHandler
from operator import itemgetter
from getpass import getpass
import json

IP = input('IP of switch: ')
username = input('Enter your username: ')
password = getpass()

SW = {
    'ip':   IP,
    'username': username,
    'password': password,
    'device_type': 'cisco_nxos',
}

net_connect = ConnectHandler(**SW)

interfaces = net_connect.send_command('show interface switchport', use_textfsm=True)
l = len(interfaces)

print(json.dumps(interfaces, indent=2))


print ('total number of interfaces are ' + str(l))