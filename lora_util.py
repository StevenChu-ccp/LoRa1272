# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:36:53 2020

@author: Steven
"""


import serial
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
    serialPort = None
    
    
    def __init__(self):
        self.a1 = 1
    
    """
    List all available ports
    return: a list of [ListPortInfo] object
    """
    def listPorts(self):        
        ports = serial.tools.list_ports.comports()
        
        for index, port in enumerate(ports):
            print("  " + str(index) + ". " + port.device)
        print(str(len(ports)) + " ports found")
        
        return ports
    
    """
    Calculate CRC by applying XOR to every bytes
    return: Hex value
    """
    def __calCRC(self, data):
        crc = 0
        for i in data:
            crc = crc^i
        return crc

    """
    Open target port
    return: [serial] object
    """
    def openPort(self, portPath):
        try:
            port = serial.Serial(portPath, 115200, timeout=3)
            return port
        except serial.SerialException as ex:
            raise OSError(ex)


    """
    Find LoRa device
    return: Full device name/path
    """
    def findLoRa(self, ports):
        for port in ports:
            self.serialPort = self.openPort(port.device)
            
            #change to __testiflora()
            data=self.GetLoRaID()
            print(data)
            if(len(data) > 1):
                return port.device
            self.serialPort.close()
            
            
        raise OSError('No LoRa device found.')
        #raise OSError
        
    
    """
    Get the details of the device
    return: Hex data
    """
    def GetLoRaID(self):
        packet_hdr = [0x80, 0x00, 0x00, 0]
        packet_hdr[3] = self.__calCRC(packet_hdr)
        if self.debug == True:
            print(packet_hdr)
        
        self.serialWrite(packet_hdr)
        
        time.sleep(0.01)
        bytesToRead = self.serialPort.inWaiting()
        data = self.serialPort.read(bytesToRead)
        if self.debug == True:
            print(data.hex())
        tmp = 0x00
        hex_digits = 0xffffff
        
        #not a good way to check byte
        if(len(data) > 5):
            # Transform the deviceID
            for i in range(5, len(data)-1):
                tmp = tmp + (data[i] * hex_digits)
                hex_digits = hex_digits / 0xff
            self.deviceID = int(tmp)
            self.firmwareVersion = data[4]  #(data[4].hex(), 16)
        return data.hex()
    
    
    """
    Write data to serial
    """
    def serialWrite(self, data):
        try:
            self.serialPort.write(serial.to_bytes(data))
        except serial.SerialExecption as ex:
            raise OSError(ex)