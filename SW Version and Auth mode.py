import json
from netmiko import ConnectHandler
from operator import itemgetter
from getpass import getpass
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

username = input('Enter your username: ')
password = getpass()

with open('H:\Scripts\TEXTFSM\device_file.txt') as f:
    devices_list = f.read().splitlines()

device_details = {}

for devices in devices_list:
    ip_address_of_device = devices
    SW = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device, 
        'username': username,
        'password': password
    }
#because you may get a timeout or the switch just does not want to respond
    try:
        net_connect = ConnectHandler(**SW)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

    
# I send out the show version and just want the hostname and version and I want to know legacy or new-style
    outputs = net_connect.send_command('show version', use_textfsm=True)

    #print(json.dumps(output, indent=2))

    output1 = net_connect.send_command('authentication display config-mode')

    #print(output1)

    for output in outputs:
            print( f"{output['hostname']} is running {output['version']} and is " + output1)
            results = ( f"{output['hostname']} is running {output['version']} and is " + output1)
            file = open('H:\Scripts\TEXTFSM\switches_for_nac.txt','a')

            file.write(results)
            file.close()
