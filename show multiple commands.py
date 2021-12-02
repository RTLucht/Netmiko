from MY_ATH import ME
from netmiko import ConnectHandler
import json

#Enter in the IP of the switch, username and password
IP = input('IP of switch: ')
username = ME['username']
password = ME['password']


SW = {
    'ip':   IP,
    'username': username,
    'password': password,
    'device_type': 'cisco_ios',
}

net_connect = ConnectHandler(**SW)

#This script has hardcoded voice vlan info


#does this command and looks at the structured data
interfaces = net_connect.send_command('show interfaces switchport', use_textfsm=True)
#cdp = net_connect.send_command('show interfaces switchport', use_textfsm=True)
#cdp2 = net_connect.send_command('show interfaces description', use_textfsm=True)
#print(json.dumps(interfaces, indent=2))
#print(json.dumps(cdp3, indent=2))

interface_list = []
for interface in interfaces:
    result={}
    result["interface"] = interface['interface']
    result["admin_mode"] = interface['admin_mode']
    result["access_vlan"] = interface['access_vlan']
    result["voice_vlan"] = interface['voice_vlan']
    result["trunking_vlans"] = interface['trunking_vlans']

    interface_list.append(result)

print (json.dumps(interface_list, indent=2))



interfaces1 = net_connect.send_command('show interfaces description', use_textfsm=True)
#print(json.dumps(interfaces1, indent=2))


interface_list1 = []
for interface in interfaces1:
    result={}
    result["interface"]=interface['port']
    result["descrip"] = interface['descrip']

    interface_list1.append(result)

print (json.dumps(interface_list1, indent=2))


interfaces2 = net_connect.send_command('show lldp neighbors detail', use_textfsm=True)
print(json.dumps(interfaces2, indent=2))
interface_list2 = []
for interface in interfaces2:
    result={}
    result["interface"]=interface['local_interface']
    result["neighbor"] = interface['neighbor']

    interface_list2.append(result)

print (json.dumps(interface_list2, indent=2))

print(interface_list)
print(interface_list1)
print(interface_list2)



for key in interface_list:
    print (key)
for key in interface_list1:
    print (key)
for key in interface_list2:
    print (key)


