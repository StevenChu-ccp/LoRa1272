# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:30:40 2020

@author: Steven
"""


import lora_util

Lora = lora_util.LoRa()
print("List All Serial Ports")
ports = Lora.listPorts()