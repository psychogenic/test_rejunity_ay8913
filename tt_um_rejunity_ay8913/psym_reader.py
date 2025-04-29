'''
Created on Jul 25, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
import struct
import ttboard.log as logging
log = logging.getLogger(__name__)
from examples.tt_um_rejunity_ay8913.sample import Sample, RegisterValue
class PsYMReader:
    def __init__(self, skip_duplicate_reg_settings:bool=True):
        self._file = None 
        self.systemclock = 0
        self.samplerateHz = 0
        self.numsamps = 0
        self.current_sample_index = 0
        self._cur_sample = None
        self._last_sample = None
        self.skip_duplicate_reg_settings = skip_duplicate_reg_settings
        
    @property 
    def samples_left(self):
        return self.numsamps - self.current_sample_index
    
    def open(self, fpath:str):
        self.current_sample_index = 0
        f = open(fpath, mode='rb')
        
        v = f.read(5)
        if v[:4] != b'PSYM':
            log.error('No magic/header found!')
            return False
        
        self._file = f
        self.systemclock = struct.unpack('i', f.read(4))[0]
        log.info(f"System clock frequency should be {self.systemclock}")
        
        self.samplerateHz = self.next_byte()
        log.info(f"Sample rate {self.samplerateHz}Hz")
        self.numsamps = struct.unpack('ii', f.read(8))[0]
        log.info(f"Have {self.numsamps} samples")
        return True
    
    
    def next_byte(self):
        if not self._file:
            return -1
        return int.from_bytes(self._file.read(1), 'big')
    
    @property 
    def last_sample(self):
        return self._last_sample
    
    
    def next_registers_list(self):
        if self.current_sample_index >= self.numsamps:
            if self._file is not None:
                self._file.close()
                self._file = None
            return None
        
        numSamps = self.next_byte()
        retList = []
        for _i in range(numSamps):
            retList.append([self.next_byte(), self.next_byte()])
            
        return retList
    
    def next_sample(self):
        registerslist = self.next_registers_list()
        numSamps = len(registerslist)
        if registerslist is None or not numSamps:
            return None
        samp = Sample(self.current_sample_index, numSamps)
        for rs in registerslist:
            samp.add_register(RegisterValue(rs[0], rs[1]))
            
        self._last_sample = self._cur_sample
        self._cur_sample = samp
        return samp 
    
    def next_registers_to_set(self):
        samp = self.next_sample()
        if samp is None:
            return None
        
        allRegs = samp.registers
        if not self.skip_duplicate_reg_settings:
            return allRegs 
        
        last_samp = self.last_sample
        if last_samp is None:
            return allRegs
        
        retList = []
        for reg in allRegs:
            if (not last_samp.has_register(reg.id)) or last_samp.get_register(reg.id).value != reg.value:
                retList.append(reg) 
        
        return retList
            
        
        
        
        
        
