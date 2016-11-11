from __future__ import division
import os
from os.path import expanduser
import csv
import sys
import re
import numpy as np

# Parameters
ExptName 	= 'stim1'
SubjID 		= 1
RunID  		= 1
HitRate 	= 9*(1/16) # multiples of 1/16
FARate  	= 3*(1/16) # multiples of 1/16

# Path info
homeDirectory = expanduser("~")
dataDirectory = homeDirectory + os.sep + 'Google Drive/tACS_VWM_ALPHA/data/' + ExptName + os.sep + 's' + SubjID + os.sep + 'setupData/'
directoryFiles = os.listdir(dataDirectory)
fileName = ''

# load setup file
for file in directoryFiles:
    match = re.match('setup-run' + str(run) + '.*', file, re.M|re.I)
    if match != None:
        fileName = saveDirectory + match.group()

setupData = np.genfromtxt(fileName, delimiter=',')



# # copied from timing setup.
# #-------Store data for thisExp (ExperimentHandler)-------
# thisExp.addData('trialID', VWMTrials[i].trialID)
# thisExp.addData('Response',resp)
# if testResponse.keys != None:  # we had a response
#     thisExp.addData('RT', testResponse.rt)
# thisExp.addData('ChangeTrial', VWMTrials[i].ChangeTrial)
# thisExp.addData('nDistractors', VWMTrials[i].nDistractors)
# thisExp.addData('nTargets', VWMTrials[i].nTargets)
# thisExp.addData('Cond', VWMTrials[i].condNum)
# if VWMTrials[i].ChangeTrial == 1:
#     thisExp.addData('changeHemi', changeTargHemi)
# thisExp.addData('ChangeCond', VWMTrials[i].ChangeCond)
# thisExp.addData('leftTargs', leftTargCount)
# thisExp.addData('rightTargs', rightTargCount)
# thisExp.addData('leftDists', leftDistCount)
# thisExp.addData('rightDists', rightDistCount)
# thisExp.nextEntry()