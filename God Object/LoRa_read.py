# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:57:17 2020

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
print("Set Mode as RX")
lora.setRX()

lora.debug = False
print("-------------------")
print("Received Message")
while True:
    received = lora.read()
    if received == None:
        continue
    elif received == "remote quit":
        break
    else:
        print(received)
        print("-------------------")
        print("Read Counter")
        print(lora.readCounter())

lora.closePort()
print("End Program")