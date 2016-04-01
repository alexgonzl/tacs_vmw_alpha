import numpy as np
from math import atan2, degrees
from AppKit import NSScreen
from psychopy import visual,monitors,tools

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

# get monitor dimensions in pixels
MonitorWidth =  NSScreen.mainScreen().frame().size.width
MonitorHeight = NSScreen.mainScreen().frame().size.height
mon = monitors.Monitor('VWMTaskMonitor')
mon.setDistance(SubjDistance) # centimeters of between monitor and subject
mon.setSizePix([MonWidth,MonHeight])
mon.setWidth(MonitorWidthCM) # widht in pixels of the monitor.

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

# all measures are in degrees
class VWMObj(Object):
    """ Trial objects. """
    size = (0.1, 0.4) 
    def __init__(self,centerLoc = (0,0), orientation = 0, objID = 0):       
    	# center location tuple: (radii in deg from center of screen, theta from median)
            self.centerLoc  	= centerLoc 
            self.orientation 	= orientation
            self.objID      	= objID
    def getLoc():
        return self.centerLoc

    def getOrientation():
        return self.orientation

    def getObjID():
        return self.objID

class VWMTargetObj(VWMObj):
    def __init__(self):
        self.color = "red";
    def objType():
        print  "Target" 

class VWMDistractorObj(VWMObj):
    def __init__(self):
        self.color = "blue";
    def objType():
        print  "Distractor"         

# define trial class
class VWMTrial(object):    
    """trial properties for VWM alpha tACS """
    def __init__(self, trialID, condNum, Change):        
        self.trialID    	= trialID        
        self.condNum 		= condNum 
        self.nTargets 		= nTargetsInCond[condNum] 
        self.nDistractors 	= nDistractorsInCond[condNum] 
        self.nTotalItems 	= self.nDistractors + self.nTargets
        self.ChangeTrial 	= Change    	
    	for (obj in range(self.nTargets)):
    		self.TargetObjs[obj] = VWMTargetObj()
    	for (obj in range(self.nDistractors)):
    		self.Distractor[obj] = VWMDistractorObj()

# Set trial conditions and counterbalance
TrialIDs 		= np.arange(nTrials)  # trial IDs
AvailableTrials = np.array(TrialIDs) 
TrialCondIDs   	= np.zeros(nTrials)   # individual trial condition
ChangeTrialIDs 	= np.zeros(nTrials)   # test array changes at test
nTrialObjs    	= np.zeros(nTrials,int)   # total number of trials per item

for cond in range(nConds):
    trials = np.random.choice(AvailableTrials,nTrialsPerCond,replace=False)
    TrialCondIDs[trials] = cond+1
    AvailableTrials = np.setxor1d(AvailableTrials,trials)
    ChangeTrialIDs[np.random.choice(trials,nTrialsPerCond/2,replace=False)]=1
    nTrialObjs[trials] = nTotalItemsPerCond[cond]
    
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

#Create the trials.
VWMTrials = []
for (tt in range(nTrials)):
	VWMTrials[tt] = VWMTrial(tt,TrialCondIDs[tt],ChangeTrialIDs[tt])
		cnt = 1;
		for (obj in range(VWMTrials.nTargets))
			# assign orientation and center position
			cnt +=1
		for (obj in range(VWMTrials.nDistractors))
			# assign orientation and center position
			cnt +=1

			
