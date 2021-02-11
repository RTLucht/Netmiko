from netmiko import ConnectHandler
from operator import itemgetter
from getpass import getpass
import json

#Enter in the IP of the switch, the vlan you want to remove, username and password
IP = input('IP of switch: ')
vlan = input('Vlan ID of what you want to delete: ')
username = input('Enter your username: ')
password = getpass()


SW = {
    'ip':   IP,
    'username': username,
    'password': password,
    'device_type': 'cisco_ios',
}

net_connect = ConnectHandler(**SW)



#does this command and looks at the structured data
interfaces = net_connect.send_command('show interface switchport', use_textfsm=True)


#from the structured data it adds the commands based on access, voice or trunk ports
for interface in interfaces:
    if interface['admin_mode'] == 'static access' and interface['access_vlan'] == vlan:
        config_commands = 'interface ' + interface['interface'] ,'no switchport access vlan ' +vlan
        output = net_connect.send_config_set(config_commands)
        print (output)
    elif interface['admin_mode'] == 'static access' and interface['voice_vlan'] == vlan:
        config_commands = 'interface ' + interface['interface'] ,'no switchport voice vlan ' +vlan
        output = net_connect.send_config_set(config_commands)
        print (output)
#the switch I have in the lab has a port channel and did not want to break it.
#I just want to add the vlan to trunks that are port channels and not the physical interfrace        
    elif interface['admin_mode'] == 'trunk' and not "trunk (member of bundle" in interface['mode'] and vlan in interface['trunking_vlans'][0].split(','):
        config_commands = 'interface ' + interface['interface'],'switchport trunk allowed vlan remove ' +vlan
        output1 = net_connect.send_config_set(config_commands)
        print (output1)

#This script has hardcoded voice vlan info
config_commands = ('no vlan ' + vlan)
output = net_connect.send_config_set(config_commands)
print (output)

#Saves the config
print('\n Saving the Switch configuration\n')
output = net_connect.save_config()
print(output)

#print(json.dumps(interfaces, indent=2))


