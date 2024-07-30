'''
Created on Jul 29, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

from machine import Pin
import rp2
from rp2 import PIO


from ttboard.demoboard import DemoBoard, Pins

import ttboard.logging as logging
log = logging.getLogger(__name__)



#
# Ok the AY8913 register writer
# this thing is a little pio program that does some fancy footwork
# to get around the fact that our chip input pins are split up 
# into 2 blocks
#  CHIPIN_LOW_NIBBLE  CHIPOUT_HIGH_NIBBLE  CHIPIN_HIGHNIBBLE
# so we define the pio output (which talks to the chip input) as a 12 bit thing
# then do some magic Mike dance using the ISR as a swap space, to finally 
# get our outputs right and ready for the chip input pins.
# This is done twice, so we latch the register, then the value
# appropriately, by using the side-set stuff (thankfully, those two 
# bidir pins are sequential).
# The state machine runs at 2MHz no problem, but if the program here is 
# optimized a bit, might need to tweak.
@rp2.asm_pio(autopull=True, 
             pull_thresh=16,
             out_shiftdir=PIO.SHIFT_RIGHT, fifo_join=rp2.PIO.JOIN_TX,
             in_shiftdir=PIO.SHIFT_LEFT,
             sideset_init=(PIO.OUT_LOW,)*2,
             out_init=(PIO.OUT_LOW,)*4 + (PIO.IN_LOW,)*4 + (PIO.OUT_LOW,)*4)
def ay8913writer():
    # This does work with a statemachine 
    # freq of 2MHz... from uPython, we can set registers with 
    # this in about 40us (down from close to 8 milliseconds!)
    # any issues, easiest fixes are to just reduce the freq=
    # in the SM below, see if that resolves things
    out(isr, 8)         .side(0)
    in_(isr, 4)         .side(0b11)
    mov(pins, isr)      .side(0b11)
    out(isr, 8)         .side(0)
    in_(isr, 4)         .side(0b10)
    mov(pins, isr)      .side(0b10).delay(3)



class AY8913PIO:
    '''
        PIO implementation of the AY8913 interface.
        Gives us a good deal more spead (~40us to set a register)
        
        All you need to do to use is:
        
        chip = AY8913PIO(tt)
        
        then call
        
            chip.set_register(regid, value:int)
            
        whenever you like.
    '''
    def __init__(self, tt:DemoBoard):
        self.tt = tt 
        
        # make sure our bidir is setup and the SEL bits are set to 0
        self.tt.bidir_mode = [Pins.OUT, Pins.OUT, Pins.OUT, Pins.OUT, 
                              Pins.IN,  Pins.IN,  Pins.IN,  Pins.IN]
        
        self.tt.bidir_byte = 0
        
        # now hand over control of the tt.in* pins and the two first
        # bidirs to the PIO state machine
        self.sm = rp2.StateMachine(0, ay8913writer, 
             freq=2000000,
             out_base=tt.in0.raw_pin,
             sideset_base=tt.uio0.raw_pin, in_base=tt.out0.raw_pin)
        
        self.runPIO(True)
        
        
    def runPIO(self, on:bool=True):
        self.sm.active(on)
        
    def reset(self):
        for i in range(16):
            self.set_register(i, 0)
            
    def set_register(self, reg:int, value:int):
        # the way things are shifted in, put the reg low
        # and the value high, and pass as a block of 16 bits 
        # to process
        self.sm.put((value << 8) | reg)
    
