from setup import oneTrial, VWMTrials, win, core

nTrials = len(VWMTrials)

# Runs all 368 trials
for i in range(nTrials):
    oneTrial(i)

win.close()
core.quit()
