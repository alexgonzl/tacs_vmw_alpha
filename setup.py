import numpy as np
from math import atan2, degrees
from AppKit import NSScreen
from psychopy import visual,monitors,tools
from psychopy.tools import coordinatetools as coord
import random

# Constants
SubjDistance 	= 100.0  # in cm
MonitorWidthCM 	= 27.94  # in cm
nTrials  	 	= 720
# Targets and distractors sets
TargetSets      = np.array([2,4])
DistractorSets  = np.array([0,2,4])
# Set orientations and location for each item
PossibleObjOrientations  = np.concatenate((np.arange(10,81),np.arange(100,171)));
PossibleObjRadix 		 = np.array([0.2, 0.4])
PossibleObjTheta         = np.concatenate((np.arange(20,71),np.arange(110,161), \
                                           np.arange(200,251),np.arange(290,341)));

# Define target and distractor location rules
maxNumObjsPerQuadrant    = 2
maxNumTargersPerQuadrant = 1
maxNumObjsPerRadix       = 4

# get monitor dimensions in pixels
MonitorWidth =  NSScreen.mainScreen().frame().size.width
MonitorHeight = NSScreen.mainScreen().frame().size.height
mon = monitors.Monitor('VWMTaskMonitor')
mon.setDistance(SubjDistance) # centimeters of between monitor and subject
mon.setSizePix([MonWidth,MonHeight])
mon.setWidth(MonitorWidthCM) # width in pixels of the monitor.

# set window
win = visual.Window(size=(500, 500), fullscr=False, screen=0, allowGUI=False, allowStencil=False,
                    monitor='VWMTaskMonitor', color=[0,0,0], colorSpace='rgb', blendMode='avg')

nConds = TargetSets.size*DistractorSets.size
nTrialsPerCond = nTrials/nConds

# condition dictionaries
conds 				= {}
nTotalObjsPerCond 	= {}
nTargetsInCond 		= {}
nDistractorsInCond 	= {}
cnt = 1;
for ts in range(TargetSets.size):
    for ds in range(DistractorSets.size):
        conds[cnt] 				= 'nT' + str(TargetSets[ts]) + 'nD' + str(DistractorSets[ds])
        nTargetsInCond[cnt] 	= TargetSets[ts]
        nDistractorsInCond[cnt] = DistractorSets[ds]
        nTotalObjsPerCond[cnt] 	= int(nTargetsInCond[cnt]+nDistractorsInCond[cnt])
        cnt += 1

def getQuadrant(theta):
    theta = theta%360
    if (theta>=0 and theta<90):
        return 1
    elif (theta>=90 and theta<180):
        return 2
    elif (theta>=180 and theta<270):
        return 3
    elif (theta>=270 and theta<360):
        return 4


# all measures are in degrees
class VWMObj():
    """ Trial objects. """
    size = (0.1, 0.4)
    def __init__(self, objtype, objID , centerLoc = (0,0), orientation = 0):
        # center location tuple: (radii in deg from center of screen, theta from median)
        if objtype=='target':
            self.color      = 'red'
        elif objtype=='distractor':
                self.color      = 'blue'
        else:
            self.color      = 'black'
            
        self.centerLoc      = centerLoc
        self.orientation    = orientation
        self.objID          = objID
        self.objType        = objtype
        self.rect           = visual.Rect(win=win, name=None,
                                              width=self.size[0], height=self.size[1], ori=orientation,
                                              pos=centerLoc, lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
                                              fillColor=self.color, fillColorSpace='rgb', opacity=1,depth=-1.0,)
        
    def getLoc(self):
        return self.centerLoc

    def getOrientation(self):
        return self.orientation
    
    def getObjID(self):
        return self.objID
    
    def getColor(self):
        return self.color
    
    def objType(self):
        return self.objtype

# define trial class
class VWMTrial():
    """trial properties for VWM alpha tACS """
    def __init__(self, trialID, condNum, Change):
        self.trialID    	= trialID
        self.condNum 		= condNum
        self.nTargets 		= nTargetsInCond[condNum]
        self.nDistractors 	= nDistractorsInCond[condNum]
        self.nTotalItems 	= self.nDistractors + self.nTargets
        self.ChangeTrial 	= Change
        self.Objects        = []
        cnt = 0
        for obj in range(self.nTargets):
            self.Objects.append(VWMObj('target',cnt))
            cnt+=1
        for obj in range(self.nDistractors):
            self.Objects.append(VWMObj('distractor',cnt))
            cnt+=1

# Set trial conditions and counterbalance
TrialIDs 		= np.arange(nTrials)  # trial IDs
AvailableTrials = np.array(TrialIDs)
TrialCondIDs   	= np.zeros(nTrials)   # individual trial condition
ChangeTrialIDs 	= np.zeros(nTrials)   # test array changes at test
nTrialObjs    	= np.zeros(nTrials,int)   # total number of trials per item

for cond in conds:
    trials = np.random.choice(AvailableTrials,nTrialsPerCond,replace=False)
    TrialCondIDs[trials] = cond
    AvailableTrials = np.setxor1d(AvailableTrials,trials)
    ChangeTrialIDs[np.random.choice(trials,nTrialsPerCond/2,replace=False)]=1
    nTrialObjs[trials] = nTotalObjsPerCond[cond]

assert AvailableTrials.size==0, 'Error Assigning Trials'
hist=np.histogram(TrialCondIDs,range(1,nConds+2))[0]
assert sum(hist==nTrialsPerCond)==nConds, 'Uneven Trials'

# set orietantions
ObjectOrietations = {};
for tt in range(nTrials):
    ObjectOrietations[tt] = np.random.choice(PossibleOrientations,nTrialItems[tt])
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