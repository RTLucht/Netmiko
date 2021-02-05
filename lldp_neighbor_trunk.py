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


l = len(interfaces and lldp)

for interface in interfaces:
    for local_interface in lldp:


        if interface['mode'] == 'trunk' and interface['interface'] == local_interface['local_interface']:
            config_commands = 'interface ' + interface['interface'],'description to ' + local_interface['neighbor']
            output1 = net_connect.send_config_set(config_commands)
            print (output1)

#Saves the config
print('\n Saving the Switch configuration\n')
output = net_connect.save_config()
print(output)

#print(json.dumps(interfaces, indent=2))

#print(json.dumps(lldp, indent=2))
