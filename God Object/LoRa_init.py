# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 16:15:06 2020

@author: Steven
"""


import lora_util

print("Print all active port")
ports = lora_util.listPorts()

print("-------------------")
lora = lora_util.LoRa()
print("Find LoRa device")
port_path = lora.findLoRa(ports)

print("-------------------")
print("Connect LoRa")
lora.ser = lora.openPort(port_path)

print("-------------------")
print("Get LoRa Info")
lora.getLoRaInfo()

print("-------------------")
print("Initialize LoRa")
lora.resetLoRa()

lora.closePort()
