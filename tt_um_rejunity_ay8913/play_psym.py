'''
Created on Jul 25, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

from ttboard.demoboard import DemoBoard

import ttboard.log as logging
log = logging.getLogger(__name__)

from examples.tt_um_rejunity_ay8913.psym_reader import PsYMReader
from examples.tt_um_rejunity_ay8913.ay8913 import AY8913
from examples.tt_um_rejunity_ay8913.ay8913PIO import AY8913PIO
from examples.tt_um_rejunity_ay8913.setup import setup
import ttboard.util.time as time 

DefaultFile = '/drwho.psym'
def runPurePython(file_to_play:str=DefaultFile):
    tt = DemoBoard.get()
    if not setup(tt):
        return False 
    reader = PsYMReader()
    if not reader.open(file_to_play):
        print(f"Could not open {file_to_play}!")
        return False 
    
    chip = AY8913(tt)
    return playLoop(reader, chip)
    

def run(file_to_play:str=DefaultFile):
    tt = DemoBoard.get()
    if not setup(tt):
        return False 
    
    return play(file_to_play)
    
    
def play(file_to_play:str=DefaultFile):
    
    reader = PsYMReader()
    if not reader.open(file_to_play):
        print(f"Could not open {file_to_play}!")
        return False 
    
    chip = AY8913PIO(DemoBoard.get())
    return playLoop(reader, chip)


def playLoopOO(reader:PsYMReader, chip):
    delayMs = int(1000/reader.samplerateHz)
    while reader.samples_left:
        tnow = time.ticks_us()
        next_reg_settings = reader.next_registers_to_set()
        if next_reg_settings is None:
            return True
        for reg in next_reg_settings:
            chip.set_register(reg.id, reg.value)
        #log.info('-')
        msToWait = int(delayMs - ((time.ticks_us() - tnow)/1000))
        #print(msToWait)
        if msToWait > 0:
            time.sleep_ms(msToWait) 
    return True
    
    
def playLoop(reader:PsYMReader, chip):
    delayMs = int(1000/reader.samplerateHz)
    while reader.samples_left:
        tnow = time.ticks_us()
        next_reg_settings = reader.next_registers_list()
        if next_reg_settings is None or not len(next_reg_settings):
            return True
        for reg in next_reg_settings:
            chip.set_register(reg[0], reg[1])
        #log.info('-')
        msToWait = int(delayMs - ((time.ticks_us() - tnow)/1000))
        #print(msToWait)
        if msToWait > 0:
            time.sleep_ms(msToWait) 
    return True
    
