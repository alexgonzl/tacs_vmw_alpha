# imports for conditionSetup
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
import numpy as np
from psychopy import data
from psychopy.tools import coordinatetools as coord
import os
from os.path import expanduser
import sys
sys.dont_write_bytecode = True
import cPickle as pickle
# import relevant classes and dicts for condition names + targets/distractors per condition
from vwmClasses import VWMObj, VWMTrial, conds, nTotalObjsPerCond, nDistractorsInCond, nTargetsInCond

### Assign Random Seed ###
assert len(sys.argv) == 3, "Too many inputs"
assert sys.argv[1].isdigit() and sys.argv[2].isdigit(), "Integers necessary"
subjHash = (int(sys.argv[1]), int(sys.argv[2]))
np.random.seed(seed=subjHash)

############# Object Location Rules ########################
# maxNumObjsPerQuadrant    = 2
# maxNumTargersPerQuadrant = 1
# maxNumObjsPerRadix       = 4
############################################################

####### Constants ######
nTrials         = 368
behavRun = 'stim1'
oriConstraint = True
rotation = 45

# Set orientations and location for each item
if oriConstraint:
    if rotation == 30:
        PossibleObjOrientations = range(3,28) + range(33,58) + range(63,88) + range(93,118) + range(123,148) + range(153,178)
    elif rotation == 45:
        PossibleObjOrientations = range(4,42) + range(49,87) + range(94,132) + range(139,177)
    elif rotation == 90:
        PossibleObjOrientations = range(10,81)+ range(100,171)
else:
    PossibleObjOrientations  = range(1,181)
PossibleObjRadix         = np.array([4, 8])
PossibleObjTheta         = np.vstack((np.arange(20,71),np.arange(110,161), \
                                    np.arange(200,251),np.arange(290,341)))

# dictionary for # of trials and # of subcondtions
nTrialsPerCond       = {1:44, 2:96, 3:44, 4:50, 5:84, 6:50}
nSubCondsPerCond     = {1:4,2:16,3:4,4:1,5:4,6:1}
assert sum(nTrialsPerCond.values()) == nTrials
# eg. conditon 1 has 4 subconditions related target/distractor positioning

# integer division for number of trials per subcondition
nTrialsPerSubCond    = {}
for cond in nTrialsPerCond.keys():
    assert nTrialsPerCond[cond] % nSubCondsPerCond[cond] == 0, "nTrialsPerCond not divisible by nSubCondsPerCond"
    nTrialsPerSubCond[cond] = int(nTrialsPerCond[cond]/nSubCondsPerCond[cond])

# make filenames based on date and terminal input
date = data.getDateStr()
homeDirectory = expanduser("~")
saveDirectory = homeDirectory + os.sep + 'Google Drive/tACS_VWM_ALPHA/data'
filename = saveDirectory + os.sep + behavRun + os.sep + 's' + sys.argv[1] + os.sep + 'setupData/setup-run' + sys.argv[2] + "_" + date
pickleFilename = saveDirectory + os.sep + behavRun + os.sep + 's' + sys.argv[1] + os.sep + 'setupData/subj' + sys.argv[1] + 'run' + sys.argv[2] + '.p'

# ExperimentHandler conducts data saving
thisExp = data.ExperimentHandler(name='setup', version='', runtimeInfo=None,
    originPath=None,
    savePickle=False, saveWideText=True,
    dataFileName=filename)

# sub-condition target/distractors pairings; note that these are all indexed/key by condition
CondsTargetQuadrants = {}
CondsDistraQuadrants = {}

# Quadrant pairings and groupings for a trial
allquads        		= np.array([1,2,3,4],np.int)
quadPairings            = np.array([[1,3],[2,4],[2,3],[1,4]],np.int) # avoids (1,2), (3,4) pairings
for cond in conds:
    nn = nSubCondsPerCond[cond]
    if cond==1: # 2 targets 0 distractors (4 sub-conditions)
        CondsTargetQuadrants[cond]  = quadPairings
        CondsDistraQuadrants[cond]  = np.zeros([nn,2],np.int)
    elif cond==2: # 2 targets 2 distractors (16 sub-conditions)
        n=quadPairings.shape[0];
        CondsTargetQuadrants[cond] = np.zeros([nn,2],np.int)
        CondsDistraQuadrants[cond] = np.zeros([nn,2],np.int)
        subcond = 0
        for jj in range(n):
            for ii in range(n):
                CondsTargetQuadrants[cond][subcond] = quadPairings[jj]
                CondsDistraQuadrants[cond][subcond] = quadPairings[ii]
                subcond +=1
    elif cond==3: # 2 targets 4 distractors (4 sub-conditions)
        CondsTargetQuadrants[cond] = np.array(quadPairings)
        CondsDistraQuadrants[cond] = np.tile(allquads,(4,1))
    elif cond==4: # 4 targets 0 distractors (1 sub-conditions)
        CondsTargetQuadrants[cond] = np.array([allquads])
        CondsDistraQuadrants[cond] = np.zeros([nn,2],np.int)
    elif cond==5: # 4 targets, 2 distractors (4 sub-conditions)
        CondsTargetQuadrants[cond] = np.tile(allquads,(4,1))
        CondsDistraQuadrants[cond] = np.array(quadPairings)
    elif cond==6: # 4 targets 4 distractors (1 sub-conditions)
        CondsTargetQuadrants[cond] = np.array([allquads])
        CondsDistraQuadrants[cond] = np.array([allquads])

# Set trial conditions and counterbalance
TrialIDs        = np.arange(nTrials)  # trial IDs
AvailableTrials = np.array(TrialIDs,np.int)
TrialCondIDs    = np.zeros(nTrials,np.int)   # individual trial condition
TrialSubCondID  = np.zeros(nTrials,np.int)   #
ChangeTrialIDs  = np.zeros(nTrials,np.int)   # test array changes at test
nTrialObjs      = np.zeros(nTrials,np.int)   # total number of trials per item

# balance subconditions
for cond in conds:
    # assign condition to trials
    trials = np.random.choice(AvailableTrials,nTrialsPerCond[cond],replace=False)
    TrialCondIDs[trials] = cond
    ChangeTrialIDs[np.random.choice(trials,int(nTrialsPerCond[cond]/2),replace=False)] = 1
    nTrialObjs[trials] = nTotalObjsPerCond[cond]

    # assign subconditions to trials
    AvailableTrials2 = np.array(trials)
    for subcond in range(nSubCondsPerCond[cond]):
        trials2 = np.random.choice(AvailableTrials2,nTrialsPerSubCond[cond],replace=False)
        TrialSubCondID[trials2]= subcond+1
        AvailableTrials2 = np.setxor1d(AvailableTrials2,trials2)

    AvailableTrials = np.setxor1d(AvailableTrials,trials)

# set center positions, check for overlap
ObjectPositions = {}
TargetPos       = {}
DistractorPos   = {}
for tt in range(nTrials):
    cond        = int(TrialCondIDs[tt])
    subCond     = int(TrialSubCondID[tt])-1
    nT          = nTargetsInCond[cond]
    nD          = nDistractorsInCond[cond]

    TargsQuad   = CondsTargetQuadrants[cond][subCond]
    DistracQuad = CondsDistraQuadrants[cond][subCond]

    trialTargPos = []
    targRadPos   = np.empty(4)
    targRadPos[:] =np.nan
    for ii in range(nT):
        qq = TargsQuad[ii] # target quadrant
        theta = np.random.choice(PossibleObjTheta[qq-1], replace=False)
        radixID = int(np.random.random()>0.5)
        targRadPos[qq-1] = radixID
        radix = PossibleObjRadix[radixID]
        x,y = coord.pol2cart(theta, radix, units='deg')
        trialTargPos.append((x,y))

    trialDisPos = []
    for ii in range(nD):
        qq = DistracQuad[ii] # target quadrant
        theta = np.random.choice(PossibleObjTheta[qq-1], replace=False)
        if targRadPos[qq-1]==1:
            radix = PossibleObjRadix[0]
        elif targRadPos[qq-1]==0:
            radix = PossibleObjRadix[1]
        else:
            radix = PossibleObjRadix[int(np.random.random()>0.5)]

        x,y = coord.pol2cart(theta, radix, units='deg')
        trialDisPos.append((x,y))

    TargetPos[tt] = trialTargPos
    DistractorPos[tt] = trialDisPos

# set orientations
## orientations sampled at random from PossibleOrientations array
ObjectOrientations = {};
for tt in range(nTrials):
    ObjectOrientations[tt] = np.random.choice(PossibleObjOrientations,nTrialObjs[tt])

#Create the trials.
VWMTrials = []
for tt in range(nTrials):
    VWMTrials.append(VWMTrial(tt,TrialCondIDs[tt],ChangeTrialIDs[tt]))

    # assign target rotation direction
    if ChangeTrialIDs[tt]==1:
        if np.random.random()>0.5:
            VWMTrials[tt].rotation = rotation
        else:
            VWMTrials[tt].rotation = rotation * -1
    changeTargID = np.random.randint(VWMTrials[tt].nTargets, size=1)
    VWMTrials[tt].ChangeTargID = changeTargID[0]

    # Assign positions and orientations to VWMTrial object
    targCnt = 0
    distCnt = 0
    for obj in range(nTrialObjs[tt]):
        VWMTrials[tt].Objects[obj].setOrientation(ObjectOrientations[tt][obj])
        if VWMTrials[tt].ObjTarg[obj]==1:
            VWMTrials[tt].Objects[obj].setLoc(TargetPos[tt][targCnt])
            targCnt +=1
        else:
            VWMTrials[tt].Objects[obj].setLoc(DistractorPos[tt][distCnt])
            distCnt +=1

# save setup info for reference
for i in range(nTrials):
    thisExp.addData('TrialID', TrialIDs[i])
    thisExp.addData('ChangeTrial', ChangeTrialIDs[i])
    thisExp.addData('TrialCond', TrialCondIDs[i])
    thisExp.addData('SubCond', TrialSubCondID[i])
    thisExp.nextEntry()

# store VWMTrials data structure in a pickle
pickle.dump(VWMTrials, open(pickleFilename, "w" ) )
