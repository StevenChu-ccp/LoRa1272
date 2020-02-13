# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:36:53 2020

@author: Steven
"""


import serial
from serial import SerialException
import serial.tools.list_ports
import platform
import time
import sys
import glob
import queue
import threading


class LoRa:
    deviceID = 10
    waitTillResponseTime = 5
    debug = True
    sleep = 0
    firmwareVersion = 0
    waitCount = 99999
    segLen = 16
    lastData = []
    
    
    def __init__(self):
        self.a1 = 1
    
    
    """
    Function for checking all available ports
    """
    def listPorts(self):        
        ports = serial.tools.list_ports.comports()
        
        for index, port in enumerate(ports):
            print("  " + str(index) + ". " + port.device)
        print(str(len(ports)) + " ports found")
        
        return ports