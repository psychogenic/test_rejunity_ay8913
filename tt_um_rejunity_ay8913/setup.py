'''
Created on Jul 30, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

from ttboard.demoboard import DemoBoard

import ttboard.log as logging
log = logging.getLogger(__name__)

import ttboard.util.platform as platform

def setup(tt:DemoBoard):
    
    if tt.shuttle.run != 'tt05':
        log.error(f"ay8913 isn't actually on shuttle {tt.shuttle.run}, sorry!")
        return False
    
    log.info("Selecting ay8913 project")
    tt.shuttle.tt_um_rejunity_ay8913.enable()

    
    tt.reset_project(True)
    #tt.clock_project_PWM(1.79e6)
    platform.set_RP_system_clock(126e6)
    tt.clock_project_PWM(2e6)

    tt.reset_project(False)
    
    return True
