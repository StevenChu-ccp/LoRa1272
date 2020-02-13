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
    def serial_allPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i+1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        ports = ['dev/tty.Bluetooth-Incoming-Port']
        for port in ports:
            try:
                if port == 'dev/tty.Bluetooth-Incoming-Port':
                    device = 1
                else:
                    device = serial.Serial(port)
                    device.close()
                    result.append(port)
            except:
                pass
        return result
    
    """
    Function for checking all available ports
    """
    def new_serial_allPorts(self):        
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            print(port)