# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:36:53 2020

@author: Steven
"""


import serial
import serial.tools.list_ports
import time
import re
import math


class LoRa:
    deviceID = 10
    chip = ""
    debug = True
    sleep = 0
    firmwareVersion = 0
    segLen = 32
    prevDataID = bytes([0, 0])
    ser = None
    chipVer = {0xc1: "Sx1272", 0xc2: "Sx1276"}
    
    
    def __init__(self):
        pass        
    
    
    """
    Open target port
    return: [serial] object
    """
    def openPort(self, portPath):
        port = serial.Serial(portPath, 115200, timeout=3)
        return port
            
    
    """
    Close serial port
    """
    def closePort(self):
        self.setStandby()
        self.ser.close()
        
    
    """
    Write data to serial
    """
    def serialWrite(self, data):
        try:
            self.ser.write(serial.to_bytes(data))
        except serial.SerialException as ex:
            raise OSError(ex)
            

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
    Check the header from response by regex
    """
    def check_header(self, pattern, string):
        if type(re.match(pattern, string)) ==  re.Match:
            return True
        else:
            return False


    """
    Find LoRa device
    return: Full device name/path
    """
    def findLoRa(self, ports):
        for port in ports:
            self.ser = self.openPort(port.device)
            if self.ser == None:
                continue
            
            data = self.pingLoRa()
            #Check returned header
            if self.check_header("^808006(c1|c2)", data.hex()) == True:
                self.closePort()
                return port.device
            self.closePort()
        raise OSError('No LoRa device found.')
        
    
    """
    Communicate with LoRa
    """
    def sendByteToChip(self, data):
        try:
            if self.debug == True:
                print("Command: " + str(bytes(data)))
            self.serialWrite(data)
            time.sleep(0.02)
            bytesToRead = self.ser.inWaiting()
            readData = self.ser.read(bytesToRead)
            if self.debug == True:
                print("Response: " + readData.hex())
            return readData
        except serial.SerialException as ex:
            raise OSError(ex)
            
            
    """
    Ping LoRa device
    return: Hex data
    """
    def pingLoRa(self):
        getIDCmd = [0x80, 0x00, 0x00, 0]
        getIDCmd[3] = self.__calCRC(getIDCmd)
        data = self.sendByteToChip(getIDCmd)
        tmp = 0x00
        hex_digits = 0xffffff
        
        #not a good way to check byte
        if(len(data) > 5):
            # Transform the deviceID
            for i in range(5, len(data)-1):
                tmp = tmp + (data[i] * hex_digits)
                hex_digits = hex_digits / 0xff
            self.chip = self.chipVer[data[3]]
            self.deviceID = data[5:9].hex()
            self.firmwareVersion = int(data[4])
        return data
    
    
    def getLoRaInfo(self):
        print("Chip = " + self.chip)
        print("Firmware Version = " + str(self.firmwareVersion))
        print("Device ID = " + str(self.deviceID))
    
    
    ##################################################
    #Application
    ##################################################
    
    """
    Initialize and reset
    """
    def resetLoRa(self):
        resetCmd = [0xC1, 0x01, 0x00, 0]
        resetCmd[3] = self.__calCRC(resetCmd)
        data = self.sendByteToChip(resetCmd)
        return data
    
    
    def getStatus(self):
        getCmd = [0xc1,0x02,0x00,0]
        getCmd[3] = self.__calCRC(getCmd)
        data = self.sendByteToChip(getCmd)
        return data
    
    
    def setRX(self):
        rxCmd = [0xC1,3,5,3,1,0x65,0x6C,0x0f,0]
        rxCmd[8] = self.__calCRC(rxCmd)
        data=self.sendByteToChip(rxCmd)
       
        #initialize prevDataID
        self.prevDataID = self.readCounter()
        return data


    def setTX(self):
        txCmd = [0xC1,3,5,2,1,0x65,0x6C,0x0f,0]
        txCmd[8] = self.__calCRC(txCmd)
        data = self.sendByteToChip(txCmd)
        return data
   
    
    def setStandby(self):
        standbyCmd = [0xC1,3,5,1,1,0x65,0x6C,0x0f,0]
        standbyCmd[8] = self.__calCRC(standbyCmd)
        data = self.sendByteToChip(standbyCmd)
        return data
    
    
    def setSleep(self):
        sleepCmd = [0xC1,3,5,0,1,0x65,0x6C,0x0f,0]
        sleepCmd[8] = self.__calCRC(sleepCmd)
        data = self.sendByteToChip(sleepCmd)
        return data
    
    
    """
    Return string
    """
    def get(self):
        getCmd = [0xc1, 0x06, 0x00, 0]
        getCmd[3] = self.__calCRC(getCmd)
        data = self.sendByteToChip(getCmd)
        
        content = str()
        #check package header
        package_hdr = self.check_header("^(c1|c2)86", data.hex())
        if package_hdr == True and len(data) > 6:
            content_len = data[2]
            #check content length, discard 2 bytes of Rssi
            if content_len > 2 and content_len <= (self.segLen + 2):
                for i in range(3, content_len + 1):
                    content += chr(data[i])
                return content
        return None
    
    
     # 讀取LoRa 是否有新的資料 (　限firmwareVersion>=5 才有的功能)
    def readCounter(self):
        cntCmd = [0xC1,0x7,0x0,0]
        cntCmd[3] = self.__calCRC(cntCmd)
        data = self.sendByteToChip(cntCmd)
        return data[3:5]
       
    
    # send string to other LoRa
    def put(self, content):
        if len(content) > self.segLen:
            print("Too much words!")
            return
        else:
            putCmd = [0xc1,0x05]
            putCmd.append(len(content))
            
            #turn string into ascii
            for letter in content:
               putCmd.append(ord(letter))
               
            CRC = self.__calCRC(putCmd)
            putCmd.append(CRC)
            
            while True:
                data = self.sendByteToChip(putCmd)
                time.sleep(self.sleep)
                #check message sent succesfully
                if self.check_header("^(c1|c2)aa0155(3f|3c)", data.hex()) == True:
                    break
            return data
    
    
    """
    Slicing content into different package
    if content length is greater than segment length
    """
    def write(self, content):
        slices = math.ceil(len(content) / self.segLen)
        for section in range(slices):
            start = section * self.segLen
            end = start + self.segLen
            data = self.put(content[start:end])
            time.sleep(0.1)
        return data

            
    """
    Read and identify if the message is repeated or not
    """
    def read(self):
        if self.prevDataID != self.readCounter():
            data = self.get()
            self.prevDataID = self.readCounter()
            if self.debug == True:
                print(self.prevDataID)
            return data
        else:
            return None
        
        
"""
List all available ports
return: a list of [ListPortInfo] object
"""
def listPorts():        
    ports = serial.tools.list_ports.comports()
    for index, port in enumerate(ports):
        print("  " + str(index+1) + ". " + port.device)
    print(str(len(ports)) + " ports found")
        
    return ports