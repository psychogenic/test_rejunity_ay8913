'''
Created on Jul 30, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

from ttboard.demoboard import DemoBoard

import ttboard.log as logging
log = logging.getLogger(__name__)

from examples.tt_um_rejunity_ay8913.ay8913 import AY8913
from examples.tt_um_rejunity_ay8913.ay8913PIO import AY8913PIO
from examples.tt_um_rejunity_ay8913.setup import setup
import ttboard.util.time as time 

def runPurePython(list_to_play, sample_rate_hz:int=50):
    tt = DemoBoard.get()
    if not setup(tt):
        return False 
    
    chip = AY8913(tt)
    return playLoop(list_to_play, sample_rate_hz, chip)
    

def run(list_to_play, sample_rate_hz:int=50):
    tt = DemoBoard.get()
    if not setup(tt):
        return False 
    
    chip = AY8913PIO(tt)
    return playLoop(list_to_play, sample_rate_hz, chip)
    
    
def playLoop(list_to_play, sample_rate_hz, chip):
    delayUs = int(1e6/sample_rate_hz)
    for samp in list_to_play:
        tnow = time.ticks_us()
        for regval in samp:
            chip.set_register(regval[0], regval[1])
        #log.info('-')
        usToWait = int(delayUs - ((time.ticks_us() - tnow)))
        #print(msToWait)
        if usToWait > 0:
            time.sleep_us(usToWait) 
    return True
    
