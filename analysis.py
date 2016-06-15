# K = S * (H - F)

import csv
from psychopy import data
import os  # handy system and path functions
import sys # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

targ2 = {}
n2targ = 0
targ4 = {}
n4targ = 0
expName = ''
expParticipant = ''
expDate = ''
with open('_tacsVWMAlpha.py_2016_May_24_2032.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
		expName = row['expName']
		expDate = row['date']
		expParticipant = row['participant']
		if row['nTargets'] == 2:
			n2targ += 1
			if row['testResponse'] == space and row['ChangeTrial'] == 1.0  and row['nDistractors'] == 0:
				targ2['hitd0'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 1.0 and row['nDistractors'] == 2:
				targ2['hitd2'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 1.0 and row['nDistractors'] == 4:
				targ2['hitd4'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 0 and row['nDistractors'] == 0:
				targ2['falsed0'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 0 and row['nDistractors'] == 2:
				targ2['falsed2'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 0 and row['nDistractors'] == 4:
				targ2['falsed4'] += 1
		else:
			n4targ += 1
			if row['testResponse'] == space and row['ChangeTrial'] == 1.0 and row['nDistractors'] == 0:
				targ4['hitd0'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 1.0 and row['nDistractors'] == 2:
				targ4['hitd2'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 1.0 and row['nDistractors'] == 4:
				targ4['hitd4'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 0 and row['nDistractors'] == 0:
				targ4['falsed0'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 0 and row['nDistractors'] == 2:
				targ4['falsed2'] += 1
			elif row['testResponse'] == space and row['ChangeTrial'] == 0 and row['nDistractors'] == 4:
				targ4['falsed4'] += 1
	
rHitt2d0 = targ2['hitd0'] / n2targ
rHitt2d2 = targ2['hitd2'] / n2targ
rHitt2d4 = targ2['hitd4'] / n2targ
rHitt4d0 = targ4['hitd0'] / n2targ
rHitt4d2 = targ4['hitd2'] / n2targ
rHitt4d4 = targ4['hitd4'] / n2targ
rFalset2d0 = targ2['falsed0'] / n2targ
rFalset2d2 = targ2['falsed2'] / n2targ
rFalset2d4 = targ2['falsed4'] / n2targ
rFalset4d0 = targ4['falsed0'] / n2targ
rFalset4d2 = targ4['falsed2'] / n2targ
rFalset4d4 = targ4['falsed4'] / n2targ
Kt2d0 = 2 * (rHitt2d0 - rFalset2d0)
Kt2d2 = 4 * (rHitt2d2 - rFalset2d2)
Kt2d4 = 6 * (rHitt2d4 - rFalset2d4)
Kt4d0 = 4 * (rHitt4d0 - rFalset4d0)
Kt4d2 = 6 * (rHitt4d2 - rFalset4d2)
Kt4d4 = 8 * (rHitt4d4 - rFalset4d4)


# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'analysis/pilotTrials'

thisExp = data.ExperimentHandler(name=expName, version='', runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

thisExp.addData('participant', expParticipant)
thisExp.addData('Kt2d0', Kt2d0)
thisExp.addData('Kt2d2', Kt2d2)
thisExp.addData('Kt2d4', Kt2d4)
thisExp.addData('Kt4d0', Kt4d0)
thisExp.addData('Kt4d2', Kt4d2)
thisExp.addData('Kt4d4', Kt4d4)
thisExp.nextEntry()

thisExp.saveAsExcel(filename, sheetName='expAnalysis', stimOut=None, dataOut=('n', 'all_mean', 'all_std', 'all_raw'), matrixOnly=False, appendFile=True, fileCollisionMethod='rename')
