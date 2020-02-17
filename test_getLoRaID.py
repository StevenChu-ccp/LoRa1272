# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 18:48:37 2020

@author: Steven
"""


import lora_util

lora = lora_util.LoRa()
ports = lora.listPorts()
lora_path = lora.findLoRa(ports)
lora.openPort(lora_path)

print(lora.getLoRaID())
print(lora.deviceID)
print(lora.firmwareVersion)

lora.serialClose()