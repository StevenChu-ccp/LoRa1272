# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:59:56 2020

@author: Steven
"""


import unittest
import sxCmd

class test_cmd(unittest.TestCase):
    
    def test_ping(self):
        lora = sxCmd.sxCmd("COM5")
        self.assertTrue(lora.ping())
        
    def test_getStatus(self):
        lora = sxCmd.sxCmd("COM5")
        self.assertTrue(lora.get_status())
        
    def test_reset(self):
        lora = sxCmd.sxCmd("COM5")
        self.assertTrue(lora.reset())
        lora.get_status()
        self.assertEqual(lora.mode, 0x01)
        self.assertEqual(lora.freq, 91500)
        self.assertEqual(lora.power, 0x00)
      
    def test_setting(self):
        lora = sxCmd.sxCmd("COM5")
        self.assertTrue(lora.setting(mode=0x01, freq=90000))
        self.assertEqual(lora.mode, 0x01)
        self.assertEqual(lora.freq, 90000)
        self.assertFalse(lora.setting(mode=6))
    
if __name__ == "__main__":
    unittest.main()