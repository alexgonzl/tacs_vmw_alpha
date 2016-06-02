# K = S * ((H - F) / (1 - F))

import csv
from psychopy import data

# Data file name stem
filename = 'analysis/pilotTrials'

thisExp = data.ExperimentHandler(name='dataAnalysis', version='', runtimeInfo=None,
	    originPath=None,
	    savePickle=True, saveWideText=True,
	    dataFileName=filename)

dataSheets = ['_tacsVWMAlpha.py_2016_May_26_1504_2.csv', '_tacsVWMAlpha.py_2016_May_26_1600.csv', 
'_tacsVWMAlpha.py_2016_May_26_1620.csv', '_tacsVWMAlpha.py_2016_May_26_1639.csv', '_tacsVWMAlpha.py_2016_May_26_1700.csv', 
'_tacsVWMAlpha.py_2016_May_26_1720.csv', '_tacsVWMAlpha.py_2016_May_26_1739.csv']

for sheet in dataSheets:
	targ2 = {}
	targ2['hitd0'] = 0
	targ2['hitd2'] = 0
	targ2['hitd4'] = 0
	targ2['falsed0'] = 0
	targ2['falsed2'] = 0
	targ2['falsed4'] = 0
	targ2['change'] = 0
	targ2['noChange'] = 0
	targ4 = {}
	targ4['hitd0'] = 0
	targ4['hitd2'] = 0
	targ4['hitd4'] = 0
	targ4['falsed0'] = 0
	targ4['falsed2'] = 0
	targ4['falsed4'] = 0
	targ4['change'] = 0
	targ4['noChange'] = 0
	expName = ''
	expParticipant = ''
	expDate = ''
	with open(sheet) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
			expName = row['expName']
			expDate = row['date']
			expParticipant = row['participant']
			if row['nTargets'] == '2':
				if row['ChangeTrial'] == '1':
					targ2['change'] += 1
				else:
					targ2['noChange'] += 1
				if row['Response key'] == 'space' and row['ChangeTrial'] == '1'  and row['nDistractors'] == '0':
					targ2['hitd0'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '1' and row['nDistractors'] == '2':
					targ2['hitd2'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '1' and row['nDistractors'] == '4':
					targ2['hitd4'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '0' and row['nDistractors'] == '0':
					targ2['falsed0'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '0' and row['nDistractors'] == '2':
					targ2['falsed2'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '0' and row['nDistractors'] == '4':
					targ2['falsed4'] += 1
			else:
				if row['ChangeTrial'] == '1':
					targ4['change'] += 1
				else:
					targ4['noChange'] += 1
				if row['Response key'] == 'space' and row['ChangeTrial'] == '1' and row['nDistractors'] == '0':
					targ4['hitd0'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '1' and row['nDistractors'] == '2':
					targ4['hitd2'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '1' and row['nDistractors'] == '4':
					targ4['hitd4'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '0' and row['nDistractors'] == '0':
					targ4['falsed0'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '0' and row['nDistractors'] == '2':
					targ4['falsed2'] += 1
				elif row['Response key'] == 'space' and row['ChangeTrial'] == '0' and row['nDistractors'] == '4':
					targ4['falsed4'] += 1	
	rHitt2d0 = float(targ2['hitd0']) / targ2['change']
	rHitt2d2 = float(targ2['hitd2']) / targ2['change']
	rHitt2d4 = float(targ2['hitd4']) / targ2['change']
	rHitt4d0 = float(targ4['hitd0']) / targ4['change']
	rHitt4d2 = float(targ4['hitd2']) / targ4['change']
	rHitt4d4 = float(targ4['hitd4']) / targ4['change']
	rFalset2d0 = float(targ2['falsed0']) / targ2['noChange']
	rFalset2d2 = float(targ2['falsed2']) / targ2['noChange']
	rFalset2d4 = float(targ2['falsed4']) / targ2['noChange']
	rFalset4d0 = float(targ4['falsed0']) / targ4['noChange']
	rFalset4d2 = float(targ4['falsed2']) / targ4['noChange']
	rFalset4d4 = float(targ4['falsed4']) / targ4['noChange']
	Kt2d0 = 2 * ((rHitt2d0 - rFalset2d0) / (1 - rFalset2d0))
	Kt2d2 = 2 * ((rHitt2d2 - rFalset2d2) / (1 - rFalset2d2))
	Kt2d4 = 2 * ((rHitt2d4 - rFalset2d4) / (1 - rFalset2d4))
	Kt4d0 = 4 * ((rHitt4d0 - rFalset4d0) / (1 - rFalset4d0))
	Kt4d2 = 4 * ((rHitt4d2 - rFalset4d2) / (1 - rFalset4d2))
	Kt4d4 = 4 * ((rHitt4d4 - rFalset4d4) / (1 - rFalset4d4))

	thisExp.addData('participant', expParticipant)
	thisExp.addData('Kt2d0', Kt2d0)
	thisExp.addData('Kt2d2', Kt2d2)
	thisExp.addData('Kt2d4', Kt2d4)
	thisExp.addData('Kt4d0', Kt4d0)
	thisExp.addData('Kt4d2', Kt4d2)
	thisExp.addData('Kt4d4', Kt4d4)
	thisExp.addData('date', expDate)
	thisExp.addData('expName', expName)
	thisExp.nextEntry()