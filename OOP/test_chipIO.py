# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 17:57:42 2020

@author: Steven
"""


import unittest
import chipIO
import time

class test_IO(unittest.TestCase):
    
    def test_open_close_Port_isOpen(self):
        port = chipIO.chipIO("COM5")
        self.assertTrue(port.is_open())
        port.closePort()
        self.assertFalse(port.is_open())
        
    def test_calCRC(self):
        port = chipIO.chipIO("COM5")
        data1 = [0x80, 0x00, 0x00]
        self.assertEqual(port._chipIO__calCRC(data1), 0x80)
        data2 = [0xc1, 0x01, 0x00]
        self.assertEqual(port._chipIO__calCRC(data2), 0xc0)
        port.closePort()
       
    def test_appendCRC(self):
        port = chipIO.chipIO("COM5")
        data1 = [0x80, 0x00, 0x00]
        self.assertEqual(port._chipIO__appendCRC(data1), [0x80, 0x00, 0x00, 0x80])
        data2 = [0xc1, 0x01, 0x00]
        self.assertEqual(port._chipIO__appendCRC(data2), [0xc1, 0x01, 0x00, 0xc0])
        port.closePort()
    
    def test_checkCRC(self):
        port = chipIO.chipIO("COM5")
        data1 = [0xc1, 0xaa, 0x01, 0x55, 0x3f]
        self.assertTrue(port._chipIO__checkCRC(data1))
        port.closePort()
    
    def test_read_write(self):
        port = chipIO.chipIO("COM5")
        init_data = [0x80, 0x00, 0x00]
        port.serialWrite(init_data)
        time.sleep(0.02)
        response = port.serialRead()
        self.assertEqual(response[:5].hex(), '808006c107')
        port.closePort()
        
    def test_sendCmd(self):
        port = chipIO.chipIO("COM5")
        init_data = [0x80, 0x00, 0x00]
        response = port.sendCmd(init_data)
        self.assertEqual(response[:5].hex(), '808006c107')
        port.closePort()

if __name__ == "__main__":
    unittest.main()