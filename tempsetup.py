import numpy as np
from math import atan2, degrees
from psychopy import visual,monitors,tools
from psychopy.tools import coordinatetools as coord
import random

# Constants
SubjDistance    = 100.0  # in cm
MonitorWidthCM  = 27.94  # in cm
nTrials         = 720 
# Targets and distractors sets
TargetSets      = np.array([2,4])
DistractorSets  = np.array([0,2,4])
# Set orientations and location for each item 
PossibleObjOrientations  = np.concatenate((np.arange(10,81),np.arange(100,171))); 
PossibleObjRadix         = np.array([0.2, 0.4])
PossibleObjTheta         = np.concatenate((np.arange(20,71),np.arange(110,161), \
                np.arange(200,251),np.arange(290,341)));

# get monitor dimensions in pixels
mon = visual.Window(size=(1280, 800), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
nConds = TargetSets.size*DistractorSets.size
nTrialsPerCond = nTrials/nConds

# condition dictionaries
conds               = {}
nTotalObjsPerCond   = {}
nTargetsInCond      = {}
nDistractorsInCond  = {}
cnt = 1;
for ts in range(TargetSets.size):
    for ds in range(DistractorSets.size):
        conds[cnt]              = 'nT' + str(TargetSets[ts]) + 'nD' + str(DistractorSets[ds])
        nTargetsInCond[cnt]     = TargetSets[ts]
        nDistractorsInCond[cnt] = DistractorSets[ds]
        nTotalObjsPerCond[cnt]  = int(nTargetsInCond[cnt]+nDistractorsInCond[cnt])
        cnt += 1     
        
# all measures are in degrees
def colorRect(color):
   polygon = visual.Rect(win=mon, name=None,
    width=0.1, height=0.4,
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=color, fillColorSpace='rgb',
    opacity=1,depth=-1.0,)
   return polygon

# define trial class
class VWMTrial(object):
    """trial properties for VWM alpha tACS """
    def __init__(self, trialID, condNum, Change):        
        self.trialID        = trialID        
        self.condNum        = condNum 
        self.nTargets       = nTargetsInCond[condNum] 
        self.nDistractors   = nDistractorsInCond[condNum] 
        self.nTotalItems    = self.nDistractors + self.nTargets
        self.ChangeTrial    = Change
        self.TargetObjs = []
        self.Distractors = []
        for obj in range(self.nTargets):
            self.TargetObjs.append(colorRect('red'))
        for obj in range(self.nDistractors):
            self.Distractors.append(colorRect('blue'))

# Set trial conditions and counterbalance
TrialIDs        = np.arange(nTrials)  # trial IDs
AvailableTrials = np.array(TrialIDs) 
TrialCondIDs    = np.zeros(nTrials)   # individual trial condition
ChangeTrialIDs  = np.zeros(nTrials)   # test array changes at test
nTrialObjs      = np.zeros(nTrials)   # total number of items per trial

for cond in range(nConds):
    trials = np.random.choice(AvailableTrials,nTrialsPerCond,replace=False)
    TrialCondIDs[trials] = cond+1
    AvailableTrials = np.setxor1d(AvailableTrials,trials)
    ChangeTrialIDs[np.random.choice(trials,nTrialsPerCond/2,replace=False)]=1
    nTrialObjs[trials] = nTotalObjsPerCond[cond + 1]
    
assert AvailableTrials.size==0, 'Error Assigning Trials'
hist=np.histogram(TrialCondIDs,range(1,nConds+2))[0]
assert sum(hist==nTrialsPerCond)==nConds, 'Uneven Trials'

# set orietantions
ObjectOrietations = {};
for tt in range(nTrials):
    ObjectOrietations[tt] = np.random.choice(PossibleObjOrientations,nTrialObjs[tt], replace=False)
##### TODO #####
##### do checks on orientations #####

##### TODO #####
# set center positions
##### do checks on center positions #####
ObjectPositions = {}
for tt in range(nTrials):
    PossibleObjPositions = []
    for i in range(int(nTrialObjs[tt])):
        radix = np.random.choice(PossibleObjRadix, replace=False)
        theta = np.random.choice(PossibleObjTheta, replace=False)
        x,y = coord.pol2cart(theta, radix, units='deg')
        PossibleObjPositions.append((x,y))
    ObjectPositions[tt] = PossibleObjPositions

#Create the trials.
VWMTrials = []
for tt in range(nTrials):
    thisTrial = VWMTrial(tt,TrialCondIDs[tt],ChangeTrialIDs[tt])
    VWMTrials.append(thisTrial)
    for obj in range(thisTrial.nTargets):
        VWMTrials[tt].TargetObjs[obj].ori = ObjectOrietations[tt][obj]
        VWMTrials[tt].TargetObjs[obj].pos = ObjectPositions[tt][obj]
    for obj in range(thisTrial.nDistractors):
        VWMTrials[tt].Distractors[obj].ori = ObjectOrietations[tt][obj+thisTrial.nTargets]
        VWMTrials[tt].Distractors[obj].pos = ObjectPositions[tt][obj+thisTrial.nTargets]

