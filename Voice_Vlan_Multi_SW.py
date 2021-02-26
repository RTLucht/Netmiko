from netmiko import ConnectHandler
from operator import itemgetter
from getpass import getpass
import json

#Enter in the IP addresses of the switches seperated by space, username and password

IP = input("Enter IP adress seperated by a space: ")
username = input('Enter your username: ')
password = getpass()
#Enter vlan info
vlan = input("Enter Voice VLAN ID: ")
vlanname = input("Enter Voice VLAN Name: ")

devices = IP.split()

device_type = 'cisco_ios'

for device in devices:
    connection = ConnectHandler(ip=device, device_type=device_type, username=username, password=password)
    interfaces = connection.send_command('show interface switchport', use_textfsm=True)
    config_commands = ['vlan '+ vlan, 'name '+ vlanname]
    output = connection.send_config_set(config_commands)
    print (output)


    for interface in interfaces:
        if interface['admin_mode'] == 'static access' and interface['access_vlan'] == 'none':
            config_commands = 'interface ' + interface['interface'] ,'switchport voice vlan ' + vlan
            output = connection.send_config_set(config_commands)
            print (output)
#the switch I have in the lab has a port channel and did not want to break it.
#I just want to add the vlan to trunks that are port channels and not the physical interfrace        
        elif interface['admin_mode'] == 'trunk' and not "trunk (member of bundle" in interface['mode']:
            config_commands = 'interface ' + interface['interface'],'switchport trunk allowed vlan add ' + vlan
            output1 = connection.send_config_set(config_commands)
            print (output1)

#Saves the config
    print('\n Saving the Switch configuration\n')
    output = connection.save_config()
    print(output)

    #print(json.dumps(interfaces, indent=2))


