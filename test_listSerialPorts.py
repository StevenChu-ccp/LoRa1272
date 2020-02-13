# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:30:40 2020

@author: Steven
"""


import lora_util

device = lora_util.LoRa()
print("List All Serial Ports")
ser = device.serial_allPorts()
print("List All Serial Ports")
newser = device.new_serial_allPorts()