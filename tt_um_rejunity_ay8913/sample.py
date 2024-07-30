'''
Created on Jul 25, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

class RegisterValue:
    def __init__(self, rid:int=0, v:int=0):
        self.id = rid
        self.value = v 
        
    def __repr__(self):
        return f'<RegValue {self.id}:{self.value}>'
        
class Sample:
    def __init__(self, idx:int, num_regs:int):
        self.index = idx;
        self._registers = {}
        
    def add_register(self, r:RegisterValue):
        self._registers[r.id] = r
        
    def has_register(self, regId:int):
        return regId in self._registers
        
    def get_register(self, regId:int):
        if self.has_register(regId):
            return self._registers[regId] 
        return None
    
    @property 
    def registers(self):
        return self._registers.values()
        
    def __repr__(self):
        return f'<Sample {self.index} ({len(self.registers)})>'

