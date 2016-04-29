import numpy as np
from math import atan2, degrees
from AppKit import NSScreen
from psychopy import visual,monitors,tools
from psychopy.tools import coordinatetools as coord
import random

# Constants
SubjDistance    = 100.0  # in cm
MonitorWidthCM  = 27.94  # in cm
nTrials         = 720
# get monitor dimensions in pixels
MonitorWidth =  NSScreen.mainScreen().frame().size.width
MonitorHeight = NSScreen.mainScreen().frame().size.height
mon = monitors.Monitor('VWMTaskMonitor')
mon.setDistance(SubjDistance) # centimeters of between monitor and subject
#mon.setSizePix([MonWidth,MonHeight]) 
mon.setWidth(MonitorWidthCM) # width in pixels of the monitor.

# set window
win = visual.Window(size=(500, 500), fullscr=False, screen=0, allowGUI=False, allowStencil=False,
                    monitor='VWMTaskMonitor', color=[0,0,0], colorSpace='rgb', blendMode='avg')

# Targets and distractors sets
TargetSets      = np.array([2,4])
DistractorSets  = np.array([0,2,4])
# Set orientations and location for each item
PossibleObjOrientations  = np.concatenate((np.arange(10,81),np.arange(100,171)));
PossibleObjRadix         = np.array([0.35, 0.85])
PossibleObjTheta         = np.vstack((np.arange(20,71),np.arange(110,161), \
                                           np.arange(200,251),np.arange(290,341)));

# Define target and distractor location rules
maxNumObjsPerQuadrant    = 2
maxNumTargersPerQuadrant = 1
maxNumObjsPerRadix       = 4

nConds = TargetSets.size*DistractorSets.size
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

# dictionary for # of trials and # of subcondtions
nTrialsPerCond       = {1:84, 2:192, 3:84, 4:100, 5:160 ,6:100}
nSubCondsPerCond     = {1:4,2:16,3:4,4:1,5:4,6:1}
nTrialsPerSubCond    = {}
for cond in conds:
    nTrialsPerSubCond[cond] = nTrialsPerCond[cond]/nSubCondsPerCond[cond]

# sub-condition target/distractors pairings; note that these are all indexed/key by condition 
CondsTargetQuadrants = {}
CondsDistraQuadrants = {}
quadTargDisOverlap   = {}

###### TODO ######
# do checks on conditions
# Possible quadrant pairings and groupings for a trial
allquadsLocs        = np.array([1,2,3,4],np.int)
quadLocs            = np.array([[1,3],[2,4],[2,3],[1,4]],np.int) # avoids (1,2), (3,4) pairings
for cond in conds:
    nn = nSubCondsPerCond[cond]    
    quadTargDisOverlap[cond]   = np.zeros([nn,4],np.int)
    if cond==1: # 2 targets 0 distractors (4 sub-conditions)        
        CondsTargetQuadrants[cond]  = quadLocs
        CondsDistraQuadrants[cond]  = np.zeros([nn,2],np.int)
    elif cond==2: # 2 targets 2 distractors (16 sub-conditions)
        n=quadLocs.shape[0];
        CondsTargetQuadrants[cond] = np.zeros([nn,2],np.int)
        CondsDistraQuadrants[cond] = np.zeros([nn,2],np.int)
        subcond = 0
        for jj in range(n): 
            for ii in range(n):
                CondsTargetQuadrants[cond][subcond] = quadLocs[jj]
                CondsDistraQuadrants[cond][subcond] = quadLocs[ii]
                for qq in range(4):
                     quadTargDisOverlap[cond][subcond][qq] =  any(CondsTargetQuadrants[cond][subcond]== qq+1) & any(CondsDistraQuadrants[cond][subcond]== qq+1)
                subcond +=1
    elif cond==3: # 2 targets 4 distractors (4 sub-conditions)
        CondsTargetQuadrants[cond] = np.array(quadLocs)
        CondsDistraQuadrants[cond] = np.tile(allquadsLocs,(4,1))
        for subcond in range(nSubCondsPerCond[cond]):
            for qq in range(4):
                     quadTargDisOverlap[cond][subcond][qq] =  any(CondsTargetQuadrants[cond][subcond]== qq+1) & any(CondsDistraQuadrants[cond][subcond]== qq+1)

    elif cond==4: # 4 targets 0 distractors (1 sub-conditions)
        CondsTargetQuadrants[cond] = np.array([allquadsLocs])
        CondsDistraQuadrants[cond] = np.zeros([nn,2],np.int)
    elif cond==5: # 4 targets, 2 distractors (4 sub-conditions)
        CondsTargetQuadrants[cond] = np.tile(allquadsLocs,(4,1))
        CondsDistraQuadrants[cond] = np.array(quadLocs)
        for subcond in range(nSubCondsPerCond[cond]):
            for qq in range(4):
                     quadTargDisOverlap[cond][subcond][qq] =  any(CondsTargetQuadrants[cond][subcond]== qq+1) & any(CondsDistraQuadrants[cond][subcond]== qq+1)
    elif cond==6: # 4 targets 4 distractors (1 sub-conditions)
        CondsTargetQuadrants[cond] = np.array([allquadsLocs])
        CondsDistraQuadrants[cond] = np.array([allquadsLocs])
        quadTargDisOverlap[cond]   = np.array([[1,1,1,1]],np.int)


# all measures are in degrees
class VWMObj():
    """ Trial objects. """
    size = (0.1, 0.3)
    def __init__(self, objType, objID , centerLoc = (0,0), orientation = 0):
    # center location tuple: (radii in deg from center of screen, theta from median)
        if objType=="target":
            self.color      = 'firebrick'
        elif objType=="distractor":
            self.color      = 'mediumblue'
        else:
            self.color      = 'black'
        
        self.centerLoc      = centerLoc
        self.orientation    = orientation
        self.objID          = objID
        self.objType        = objType
        self.rect           = visual.Rect(win=win, name=None,
                                width=self.size[0], height=self.size[1], ori=orientation,
                                pos=centerLoc, lineWidth=1, lineColor=self.color, lineColorSpace='rgb',
                                fillColor=self.color, fillColorSpace='rgb', opacity=1, depth=-1.0, interpolate=True)
    def getLoc(self):
        return self.centerLoc

    def getOrientation(self):
        return self.orientation
    
    def getObjID(self):
        return self.objID
    
    def getColor(self):
        return self.color
    
    def objType(self):
        return self.objType

# define trial class
class VWMTrial():
    """trial properties for VWM alpha tACS """
    def __init__(self, trialID, condNum, Change):
        self.trialID        = trialID
        self.condNum        = condNum
        self.nTargets       = nTargetsInCond[condNum]
        self.nDistractors   = nDistractorsInCond[condNum]
        self.nTotalItems    = self.nDistractors + self.nTargets
        self.ChangeTrial    = Change
        self.ChangeTargID   = 1
        self.ChangeTargSign = 0
        self.Objects        = []
        self.ObjTarg        = np.zeros(self.nTotalItems,np.int)
        cnt = 0
        for obj in range(self.nTargets):
            self.Objects.append(VWMObj('target',cnt))
            self.ObjTarg[cnt]=1
            cnt+=1
        for obj in range(self.nDistractors):
            self.Objects.append(VWMObj('distractor',cnt))
            self.ObjTarg[cnt]=0
            cnt+=1

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
    ChangeTrialIDs[np.random.choice(trials,nTrialsPerCond[cond]/2,replace=False)]=1
    nTrialObjs[trials] = nTotalObjsPerCond[cond]
    
    # assign subconditions to trials
    AvailableTrials2 = np.array(trials)
    for subcond in range(nSubCondsPerCond[cond]):
        trials2 = np.random.choice(AvailableTrials2,nTrialsPerSubCond[cond],replace=False)
        TrialSubCondID[trials2]= subcond+1
        AvailableTrials2 = np.setxor1d(AvailableTrials2,trials2)

    AvailableTrials = np.setxor1d(AvailableTrials,trials)

# set center positions
##### do checks on center positions #####
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
    quadOverlap = quadTargDisOverlap[cond][subCond]

    # bad code here. need to clean up #AG 4/26/16
    trialTargPos = []
    targRadPos   = np.empty(4)
    targRadPos[:] =np.nan
    for ii in range(nT):
        qq = TargsQuad[ii] # target quadrant
        theta = np.random.choice(PossibleObjTheta[qq-1], replace=False)
        radixID = int(np.random.random>0.5)
        targRadPos[qq-1] = radixID;
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
            radix = PossibleObjRadix[int(np.random.random>0.5)]

        x,y = coord.pol2cart(theta, radix, units='deg')
        trialDisPos.append((x,y))

    TargetPos[tt] = trialTargPos
    DistractorPos[tt] = trialDisPos


# set orietantions 
# orientations sampled at random from PossibleOrientations array
ObjectOrietations = {};
for tt in range(nTrials):
    ObjectOrietations[tt] = np.random.choice(PossibleObjOrientations,nTrialObjs[tt])


#Create the trials.
VWMTrials = []
for tt in range(nTrials):
    VWMTrials.append(VWMTrial(tt,TrialCondIDs[tt],ChangeTrialIDs[tt]))
    
    # TODO: change into more efficient code (this can be a one liner...)
    if ChangeTrialIDs[tt]==1:
        if np.random.random()>0.5:
            VWMTrials[tt].ChangeTargSign=1
        else:
            VWMTrials[tt].ChangeTargSign=-1

    targCnt = 0
    distCnt = 0
    for obj in range (VWMTrials[tt].nTotalItems):
        VWMTrials[tt].Objects[obj].rect.ori = ObjectOrietations[tt][obj]
        if VWMTrials[tt].ObjTarg[obj]==1: 
            VWMTrials[tt].Objects[obj].rect.pos = TargetPos[tt][targCnt]
            targCnt +=1            
        else:
            VWMTrials[tt].Objects[obj].rect.pos = DistractorPos[tt][distCnt]
            distCnt +=1