from psychopy import data
from dataFunctions import pashlerK, rtCalc
import pandas as pd

# Data file name stem
filename = 'analysis/pilotTrials'

thisExp = data.ExperimentHandler(name='dataAnalysis', version='', runtimeInfo=None,
	    originPath=None,
	    savePickle=True, saveWideText=True,
	    dataFileName=filename)

dataSheets = ['_tacsVWMAlpha.py_2016_May_26_1504_2.csv', '_tacsVWMAlpha.py_2016_May_26_1600.csv', 
'_tacsVWMAlpha.py_2016_May_26_1620.csv', '_tacsVWMAlpha.py_2016_May_26_1639.csv', '_tacsVWMAlpha.py_2016_May_26_1700.csv', 
'_tacsVWMAlpha.py_2016_May_26_1720.csv', '_tacsVWMAlpha.py_2016_May_26_1739.csv']

# aggregate K and RT values from each trial run
Kvals = []
RTs = []

for sheet in dataSheets:
    Kvals.append(pashlerK(sheet))
    RTs.append(rtCalc(sheet))

Kchart = pd.DataFrame(Kvals, index=dataSheets, columns=Kvals[0].keys())
RTchart = pd.DataFrame(RTs, index=dataSheets, columns=RTs[0].keys())
	
	
# thisExp.addData('expName', expName)
# thisExp.nextEntry()