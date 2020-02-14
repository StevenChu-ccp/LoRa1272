# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:47:07 2020

@author: Steven
"""


import lora_util

lora = lora_util.LoRa()
ports = lora.listPorts()
print(lora.findLoRa(ports))