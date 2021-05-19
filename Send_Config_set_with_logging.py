#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import errno
import time

scriptname = input('What is the configuration you want to send')

def time_stamp():
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    return t

username = input('Enter your SSH username: ')
password = getpass()

#with open('H:\Scripts\8021x\commands') as f:
 #   commands_list = f.read().splitlines()

with open('H:\Scripts\Logging Script\devices') as f:
    devices_list = f.read().splitlines()

for devices in devices_list:
    print ('Connecting to device" ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device, 
        'username': username,
        'password': password
    }

    try:
        net_connect = ConnectHandler(**ios_device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        with open("H:\Scripts\Logging Script\error.log","a") as e:
            e.write("script " + scriptname + " User " + username +" "+ time_stamp() + " " + ip_address_of_device + " Wrong credentials.\n")
        e.close()
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        with open("H:\Scripts\Logging Script\error.log","a") as e:
            e.write("script " + scriptname + " User " + username + " " + time_stamp() + " " + ip_address_of_device + " Timeout connecting to the device.\n")
        e.close()
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        with open("H:\Scripts\Logging Script\error.log","a") as e:
            e.write("script " + scriptname + " User " + username +" "+ time_stamp() + " " + ip_address_of_device + " End of file while attempting device.\n")
        e.close()
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        with open("H:\Scripts\Logging Script\error.log","a") as e:
            e.write("script " + scriptname + " User " + username +" "+ time_stamp() + " Is SSH Enabled on " + ip_address_of_device + " ?\n")
        e.close()
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        with open("H:\Scripts\Logging Script\error.log","a") as e:
            e.write("script " + scriptname + " User " + username +" "+ time_stamp() + " Unknown error on " + ip_address_of_device + " .\n")
        e.close()
        continue

    output = net_connect.send_config_set(scriptname)
    print (ip_address_of_device,output)
    with open("H:\Scripts\Logging Script\success.log","a") as s:
        s.write("script " + scriptname + " User " + username +" "+ time_stamp() + " " + ip_address_of_device + " Successfully executed commands on the host.\n")
    s.close()


