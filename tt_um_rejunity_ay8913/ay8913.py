'''
Created on Jul 25, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
from ttboard.demoboard import DemoBoard, Pins

import ttboard.util.time as time
import ttboard.log as logging
log = logging.getLogger(__name__)

def wait_clocks(num:int=1):
    for _i in range(num):
        time.sleep_us(1)
        
class AY8913:
    '''
        Pure Python implementation, sans PIO or anything fancy.
        It's clean.  It's slow.  Takes maybe 8ms to set a register
        but it does work and can act as an easy-to-debug reference.
    '''
    def __init__(self, tt:DemoBoard):
        self.tt = tt 
        self._cur_reg = -1
        self._cur_val = -1
        
        self.tt.bidir_mode = [Pins.OUT, Pins.OUT, Pins.OUT, Pins.OUT, 
                              Pins.IN,  Pins.IN,  Pins.IN,  Pins.IN]
        
        self.tt.bidir_byte = 0
        
        self.latch_delay_clocks = 0
        
        # need speed
        self._pin_bdir = self.tt.uio1.raw_pin 
        self._pin_bc1 = self.tt.uio0.raw_pin 
        
        
        
    def reset(self):
        for i in range(16):
            self.register = i 
            self.value = 0
    
    @property
    def bus(self):
        return self.tt.input_byte 
    
    @bus.setter 
    def bus(self, set_to:int):
        self.tt.input_byte = set_to
    @property 
    def bc1(self):
        return self.tt.pins.uio0()
    
    @bc1.setter 
    def bc1(self, set_to:int):
        #self.tt.pins.uio0(set_to)
        self._pin_bc1.value(set_to)
        
    @property 
    def bdir(self):
        return self.tt.pins.uio1()
    
    @bdir.setter 
    def bdir(self, set_to:int):
        #self.tt.pins.uio1(set_to)
        self._pin_bdir.value(set_to)
        
        
    @property 
    def sel0(self):
        return self.tt.pins.uio2()
    
    @sel0.setter 
    def sel0(self, set_to:int):
        self.tt.pins.uio2(set_to)
        
        
    @property 
    def sel1(self):
        return self.tt.pins.uio3()
    
    @sel1.setter 
    def sel1(self, set_to:int):
        self.tt.pins.uio3(set_to)
        
    
    def clockDivStandard(self):
        self.sel0 = 0
        self.sel1 = 0
        
    def clockDivNone(self):
        self.sel1 = 0 # set 0 first, avoid 11
        self.sel0 = 1
        
    def clockDiv128(self):
        self.sel0 = 0 # set 0 first, avoid 11
        self.sel1 = 1
        
        
        
    
    def set_register(self, reg, value):
        self.register = reg
        self.value = value
        
        
    @property 
    def register(self):
        return self._cur_reg
    
    @register.setter
    def register(self, set_to:int):
        self.bdir = 1
        self.bc1 = 1
        self.bus = set_to 
        self._cur_reg = set_to
        if self.latch_delay_clocks:
            wait_clocks(self.latch_delay_clocks * 2)
            
        self.bdir = 0 # unimplement 01
        self.bc1 = 0
        
        
    @property 
    def value(self):
        return self._cur_val
    
    @value.setter
    def value(self, set_to:int):
        self.bdir = 1
        self.bc1 = 0
        self.bus = set_to 
        self._cur_val =  set_to
        if self.latch_delay_clocks:
            wait_clocks(self.latch_delay_clocks)
        self.bdir = 0
        
        #log.info(f'Set {self.register} to {set_to}')
        
        
        
        
    
        
