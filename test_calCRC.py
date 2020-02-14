# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:24:00 2020

@author: Steven
"""


import lora_util
import unittest

class TestCRC(unittest.TestCase):
    lora = lora_util.LoRa()
    
    def test_header_package(self):
        content1 = [0x08, 0x00, 0x00, 0]
        self.assertEqual(self.lora._LoRa__calCRC(content1), 0x08)

    def test_init_package(self):
        content1 = [0xc1, 0x01, 0x00, 0]
        self.assertEqual(self.lora._LoRa__calCRC(content1), 0xc0)
        
if __name__ == '__main__':
    unittest.main()