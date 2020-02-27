# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:47:40 2020

@author: Steven
"""


from paramiko import SSHClient
from scp import SCPClient
import glob

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('192.168.0.101', 22, 'pi', 'ntou414')

scp = SCPClient(ssh.get_transport())

for file in glob.glob("*.py"):
    scp.put(file, remote_path='/home/pi/Desktop/lora_test')

scp.close()
print("Done")