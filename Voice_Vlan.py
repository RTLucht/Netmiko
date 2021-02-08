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
config_commands = ['vlan 1994', 'name Hosted_VOIP']
output = net_connect.send_config_set(config_commands)
print (output)

#does this command and looks at the structured data
interfaces = net_connect.send_command('show interface switchport', use_textfsm=True)


#from the structured data it adds the commands based on access or trunk ports
for interface in interfaces:
    if interface['admin_mode'] == 'static access'and interface['voice_vlan'] == 'none':
        config_commands = 'interface ' + interface['interface'] ,'switchport voice vlan 1994'
        output = net_connect.send_config_set(config_commands)
        print (output)
#the switch I have in the lab has a port channel and did not want to break it.
#I just want to add the vlan to trunks that are port channels and not the physical interfrace        
    elif interface['admin_mode'] == 'trunk' and not "trunk (member of bundle" in interface['mode']:
        config_commands = 'interface ' + interface['interface'],'switchport trunk allowed vlan add 1994'
        output1 = net_connect.send_config_set(config_commands)
        print (output1)

#Saves the config
print('\n Saving the Switch configuration\n')
output = net_connect.save_config()
print(output)

#print(json.dumps(interfaces, indent=2))


