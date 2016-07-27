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

### Path and Filename Information based on terminal input###
behavRun        = 'stim0'
date            = data.getDateStr()
homeDirectory   = expanduser("~")
saveDirectory   = homeDirectory + os.sep + 'Google Drive/tACS_VWM_ALPHA/data'
filename        = saveDirectory + os.sep + behavRun + os.sep + 's' + sys.argv[1] + os.sep + 'setupData/setup-run' + sys.argv[2] + "_" + date
pickleFilename  = saveDirectory + os.sep + behavRun + os.sep + 's' + sys.argv[1] + os.sep + 'setupData/subj' + sys.argv[1] + 'run' + sys.argv[2] + '.p'

# ExperimentHandler conducts data saving
thisExp = data.ExperimentHandler(name='setup', version='', runtimeInfo=None,
    originPath=None,
    savePickle=False, saveWideText=True,
    dataFileName=filename)

############# Object Location Rules ########################
# maxNumObjsPerQuadrant    = 2
# maxNumTargersPerQuadrant = 1
# maxNumObjsPerRadix       = 4
############################################################

####### Constants ######
nTrials         = 384
oriConstraint   = True
rotation        = 45

# Set orientations and location for each item
PossibleObjOrientations = []
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

# nTrials
nChangeTrials       = int(nTrials/2)
nLeftChangeTrials   = int(nChangeTrials/2)
nRightChangeTrials  = int(nChangeTrials/2)
nNoChangeTrials     = int(nTrials - nChangeTrials)

# Whole Field Conditions
WFCondNames           = {1:'t2d0',2:'t2d2',3:'t2d4',4:'t4d0',5:'t4d2',6:'t4d4'}
nWFConds              = 6;
nTrialsPerWFCond      = int(nTrials/nWFConds);
nWFSubCondsPerWFCond  = {1:2,2:8,3:2,4:1,5:4,6:1}
# sub conditions indicate possible target/distractor locations on the whole field

# integer division for number of trials per subcondition
nTrialsPerWFSubCond    = {}
for cond in WFCondNames.keys():
    assert nTrialsPerWFCond % nWFSubCondsPerWFCond[cond] == 0, "nTrialsPerCond not divisible by nSubCondsPerCond"
    nTrialsPerWFSubCond[cond] = int(nTrialsPerWFCond/nWFSubCondsPerWFCond[cond])

ChangeConds     = {1:'L',2:'R',3:'N'}
WeightPerChangeCond = {1: 0.25, 2: 0.25, 3: 0.5}
nTrialsPerChangeCond = {1:nLeftChangeTrials,2:nRightChangeTrials,3:nNoChangeTrials}
# Hemi field conditions for change trials :
HFCondNames     = {1:'t1d0',2:'t1d1',3:'t1d2',4:'t2d0',5:'t2d1',6:'t2d2'}
nHFConds        = 6
nTrialsPerHFCond   = 16
nTrialsHFChangeCons = {1: nTrialsPerHFCond, 2: nTrialsPerHFCond, 3: nTrialsPerHFCond*2}
# By design HF and WF conditions match;
# WF t2d0 is Left Change t1d0, Right Change t1d0, and No Change t1d0
# so on for the rest of the HF_ChangeConds


# sub-condition target/distractors pairings; note that these are all indexed/key by condition
CondsTargetQuadrants = {}
CondsDistraQuadrants = {}

# Quadrant pairings and groupings for a trial
allquads                = np.array([1,2,3,4],np.int)
targQuadPairings        = np.array([[1,3],[2,4]],np.int) # only diagonal pairings for targets
distQuadPairings        = np.array([[1,3],[2,4],[1,2],[3,4]],np.int) # avoids same hemisphere for distractors pairings
for cond in WFCondNames.keys():
    nn = nWFSubCondsPerWFCond[cond]
    if cond==1: # 2 targets 0 distractors (2 sub-conditions)
        CondsTargetQuadrants[cond]  = targQuadPairings
        CondsDistraQuadrants[cond]  = np.zeros([nn,2],np.int)
    elif cond==2: # 2 targets 2 distractors (8 sub-conditions)
        n1=targQuadPairings.shape[0]
        n2=distQuadPairings.shape[0]
        CondsTargetQuadrants[cond] = np.zeros([nn,2],np.int)
        CondsDistraQuadrants[cond] = np.zeros([nn,2],np.int)
        subcond = 0
        for jj in range(n1):
            for ii in range(n2):
                CondsTargetQuadrants[cond][subcond] = targQuadPairings[jj]
                CondsDistraQuadrants[cond][subcond] = distQuadPairings[ii]
                subcond +=1
    elif cond==3: # 2 targets 4 distractors (2 sub-conditions)
        CondsTargetQuadrants[cond] = np.array(targQuadPairings)
        CondsDistraQuadrants[cond] = np.tile(allquads,(4,1))
    elif cond==4: # 4 targets 0 distractors (1 sub-conditions)
        CondsTargetQuadrants[cond] = np.array([allquads])
        CondsDistraQuadrants[cond] = np.zeros([nn,2],np.int)
    elif cond==5: # 4 targets, 2 distractors (4 sub-conditions)
        CondsTargetQuadrants[cond] = np.tile(allquads,(4,1))
        CondsDistraQuadrants[cond] = np.array(distQuadPairings)
    elif cond==6: # 4 targets 4 distractors (1 sub-conditions)
        CondsTargetQuadrants[cond] = np.array([allquads])
        CondsDistraQuadrants[cond] = np.array([allquads])

# Set trial conditions and counterbalance
TrialIDs            = np.arange(nTrials)  # trial IDs
TrialWFCondIDs      = np.zeros(nTrials,np.int)  # WF trial condition
TrialHFCondsID      = np.zeros(nTrials,np.int)  # HF trial condition
TrialWFSubCondID    = np.zeros(nTrials,np.int)  # WF trial subcondition
TrialChangeCondID   = np.zeros(nTrials,np.int)  # Change Trial ID
nTrialObjs          = np.zeros(nTrials,np.int)  # total number of objects per trial

# balance subconditions
AvailableTrials     = np.array(TrialIDs,np.int)
for cond in WFCondNames.keys():
    # assign condition to trials
    trials = np.random.choice(AvailableTrials,nTrialsPerWFCond,replace=False)
    TrialWFCondIDs[trials] = cond
    TrialHFCondsID[trials] = cond
    nTrialObjs[trials] = nTotalObjsPerCond[cond-1]

    # assign subconditions to trials
    AvailableTrials2 = np.array(trials)
    for subcond in range(1,nWFSubCondsPerWFCond[cond]+1):
        trials2 = np.random.choice(AvailableTrials2,nTrialsPerWFSubCond[cond],replace=False)
        TrialWFSubCondID[trials2] = subcond

        # assign change trials
        AvailableTrials3 = np.array(trials2)
        for cc in ChangeConds.keys():
            nn      = int(nTrialsPerWFSubCond[cond]*WeightPerChangeCond[cc])
            trials3 = np.random.choice(AvailableTrials3,nn,replace=False)
            TrialChangeCondID[trials3] = cc
            AvailableTrials3 = np.setxor1d(AvailableTrials3,trials3)
        AvailableTrials2 = np.setxor1d(AvailableTrials2,trials2)
    AvailableTrials = np.setxor1d(AvailableTrials,trials)

# checks for change trial balancing
for cc in ChangeConds.keys():
    assert (sum(TrialChangeCondID==cc)==nTrialsPerChangeCond[cc])

# checks for hemifield change balancing
for cond in WFCondNames.keys():
    for cc in ChangeConds.keys():
        assert (sum((TrialWFCondIDs==cond) & (TrialChangeCondID==cc))== nTrialsHFChangeCons[cc])

# set center positions, check for overlap
ObjectPositions = {}
TargetPos       = {}
DistractorPos   = {}
# if change trial, indicate which target object is in the correct hemisphere
TargetChangeID  = np.zeros(nTrials,np.int)-1
for tt in range(nTrials):
    cond        = int(TrialWFCondIDs[tt])
    subCond     = int(TrialWFSubCondID[tt])
    nT          = nTargetsInCond[cond-1]
    nD          = nDistractorsInCond[cond-1]

    TargsQuad   = CondsTargetQuadrants[cond][subCond-1]
    DistracQuad = CondsDistraQuadrants[cond][subCond-1]

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

        if (TargetChangeID[tt]==-1) & (TrialChangeCondID[tt]<3):
            if (TrialChangeCondID[tt]==1) & (theta>=90):
                TargetChangeID[tt]=ii
            elif (TrialChangeCondID[tt]==2) & (theta<90):
                TargetChangeID[tt]=ii

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

# check that change target is on the correct hemisphere
for tt in range(nTrials):
    if TrialChangeCondID[tt]==1:
        assert TargetPos[tt][TargetChangeID[tt]][0]<0, 'left change trial counterbalancing failed'
    elif TrialChangeCondID[tt]==2:
        assert TargetPos[tt][TargetChangeID[tt]][0]>0, 'right change trial counterbalancing failed'
    else:
        assert (TrialChangeCondID[tt]==3) & (TargetChangeID[tt]==-1), 'no change counterbalancing failed'

# set orientations
## orientations sampled at random from PossibleOrientations array
ObjectOrientations = {};
for tt in range(nTrials):
    ObjectOrientations[tt] = np.random.choice(PossibleObjOrientations,nTrialObjs[tt])

#Create the trials.
VWMTrials = []
for tt in range(nTrials):
    VWMTrials.append(VWMTrial(tt,TrialWFCondIDs[tt],TrialChangeCondID[tt],TargetChangeID[tt]))

    # assign target rotation direction
    if TrialChangeCondID[tt]<3: # there is a change
        if np.random.random()>0.5:
            VWMTrials[tt].rotation = rotation
        else:
            VWMTrials[tt].rotation = rotation * -1

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
for tt in range(nTrials):
    thisExp.addData('TrialID', TrialIDs[tt])
    thisExp.addData('TrialChangeCondID', TrialChangeCondID[tt])
    thisExp.addData('TrialWFCond', TrialWFCondIDs[tt])
    thisExp.addData('WFSubCond', TrialWFSubCondID[tt])
    thisExp.addData('TrialHFCond', TrialHFCondsID[tt])
    thisExp.nextEntry()

# store VWMTrials data structure in a pickle
pickle.dump(VWMTrials, open(pickleFilename, "w" ) )
