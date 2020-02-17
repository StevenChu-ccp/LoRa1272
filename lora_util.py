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
            data=self.getLoRaID()
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
    def getLoRaID(self):
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
            
    
    """
    Communicate with LoRa
    """
    def sendByteToChip(self, data):
        try:
            if self.debug == True:
                print(data)
            self.serialPort.write(serial.to_bytes(data))
            time.sleep(0.04)
            bytesToRead = self.serialPort.inWaiting()
            cnt = 0
            while True:
                readData = self.serialPort.read(bytesToRead)
                cnt += 1
                
                #if sucess or time out, break
                if len(data) > 0 or cnt > self.waitCount:
                    break
            if self.debug == True:
                print(readData.hex())
        #except (OSError, serial.SerialException):
        except serial.SerialExecption as ex:
            raise OSError(ex)
        return readData
    
    
    """
    Close serial port
    """
    def serialClose(self):
        try:
            self.serialPort.close()
        except serial.SerialException:
            print("port already open")
            
    
    ##################################################
    #Application
    ##################################################
    
    def initLoRa(self):
        initCmd = [0xc1, 0x01, 0x00, 0]
        initCmd[3] = self.__calCRC(initCmd)
        data = self.sendByteToChip(initCmd)
        return data
    
    
    def readSetup(self):
        package_hdr = [0xc1,0x02,0x00,0]
        package_hdr[3] = self.__calCRC(package_hdr)
        data = self.sendByteToChip(package_hdr)
        return data
    
    
    def RX(self):
       array1 = [0xC1,3,5,3,1,0x65,0x6C,0x0f,0]
       array1[8] = self.__calCRC(array1)
       data=self.sendByteToChip(array1)
       return data

    # 設定寫入和頻段
    def TX(self):
       array1 = [0xC1,3,5,2,1,0x65,0x6C,0x0f,0]
       array1[8] = self.__calCRC(array1)
       data = self.sendByteToChip(array1)
       return data