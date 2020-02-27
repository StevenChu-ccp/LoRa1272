# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:10:54 2020

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

print("-------------------")
print("Get Status")
lora.getStatus()

print("-------------------")
print("Set Mode as TX")
lora.setTX()

print("-------------------")
print("Type 'QUIT' to quit program")

txt = input('Message to Sent: ')
while txt != "QUIT":
    lora.write(txt)
    txt = input('Message to Sent: ')

lora.closePort()
print("End Program")