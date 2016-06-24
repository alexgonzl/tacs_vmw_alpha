from setup import oneTrial, VWMTrials

nTrials = len(VWMTrials)

# Runs all 368 trials
for i in range(nTrials):
    oneTrial(i)

thisExp.saveAsExcel(filename, sheetName='expData', stimOut=None, dataOut=('n', 'all_mean', 'all_std', 'all_raw'), matrixOnly=False, appendFile=True, fileCollisionMethod='rename')
win.close()
core.quit()