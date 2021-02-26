from netmiko import ConnectHandler
from operator import itemgetter
from getpass import getpass
import json



IP = input("Enter IP adress seperated by a space: ")
username = input('Enter your username: ')
password = getpass()

devices = IP.split()

device_type = 'cisco_ios'

for device in devices:
    connection = ConnectHandler(ip=device, device_type=device_type, username=username, password=password)
    output = connection.send_command('show interface switchport', use_textfsm=True)
    print(json.dumps(output, indent=2))


