#MY_ATH just holds some usernames and passwords for different functions
from MY_ATH import ME
from netmiko import ConnectHandler
from operator import itemgetter
import json

# Quick Script to get how many interfaces have zero account
# Using the ntc_templates
# Some Monty Python Holy Grail fun

IP = input("IP address of Switch? ")

if input("are you sure you rally want to do this? (y/n) ") != "y":
    exit()


if input("What is your favorite color? ") != "yellow":
    exit()


sw = {
    'device_type': 'cisco_ios',
    'ip': IP,
    'username': ME["username"],
    'password': ME["password"]
}



device_list = [sw]

counts = 0
for devices in device_list:
    net_connect = ConnectHandler(**devices)
    output = net_connect.send_command('show interfaces', use_textfsm=True)
    #The below statement well show some neat things
    #print(json.dumps(output, indent=2))
    l = len(output)
    for i in range(0,l):
        if output[i]['input_packets'] == '0':
            counts += 1
print (counts,"interfaces on "+ IP + " have no input")
