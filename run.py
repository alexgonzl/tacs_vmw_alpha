from conditionSetup import win
from timingSetup import oneTrial, VWMTrials
from psychopy import core

nTrials = len(VWMTrials)

# Runs all 368 trials
for i in range(nTrials):
    oneTrial(i)

win.close()
core.quit()
