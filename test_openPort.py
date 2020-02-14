# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:37:56 2020

@author: Steven
"""


import lora_util

lora = lora_util.LoRa()

#correct port
try:
    port = ['dev/ttyACM0']
    print('Port status: ', lora.openPort(port))
except:
    print('Failed to open port ttyACM0')

#unexist port
try:
    port = ['dev/ttyACM1']
    print('Port status: ', lora.openPort(port))
except:
    print('Failed to open port ttyACM1')