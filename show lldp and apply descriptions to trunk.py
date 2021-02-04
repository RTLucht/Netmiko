from netmiko import ConnectHandler
from operator import itemgetter
from getpass import getpass
import json

#Enter in the IP of the switch, username and password
IP = input('IP of switch: ')
username = input('Enter your username: ')
password = getpass()


SW = {
    'ip':   IP,
    'username': username,
    'password': password,
    'device_type': 'cisco_ios',
}

net_connect = ConnectHandler(**SW)

#This script has hardcoded voice vlan info


#does this command and looks at the structured data
interfaces = net_connect.send_command('show interface switchport', use_textfsm=True)

lldp = net_connect.send_command('show lldp neighbors detail', use_textfsm=True)

#creates a variable of the neighbors in the show lldp neighbprs

for local_interface in lldp:
        neighbor = (lldp[0]['neighbor'])

#I just want to apply the description to trunk interfaces
for interface in interfaces:       
    if interface['admin_mode'] == 'trunk':
        config_commands = 'interface ' + interface['interface'],'description to ' + neighbor
        output1 = net_connect.send_config_set(config_commands)
        print (output1)

#print(json.dumps(interfaces, indent=2))

#print(json.dumps(lldp, indent=2))
