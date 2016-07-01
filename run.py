# imports for run
import sys
sys.dont_write_bytecode = True
from timingSetup import oneTrial, VWMTrials, win
from psychopy import core

# initialize nTrials based on VWMTrials data structure
nTrials = len(VWMTrials)

# Runs all nTrials
for i in range(nTrials):
    oneTrial(i)

# close window and quit psychopy
win.close()
core.quit()
