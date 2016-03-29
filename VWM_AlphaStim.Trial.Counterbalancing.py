
import numpy as np
# define a point in space

class VWMObj(Object):
    """ Trial objects. """
    size = (100, 400) # height and width in pixels. 
    def _init_(self,centerLoc,orientation,objID):       
            self.centerLoc  = centerLoc
            self.orientation = orientation
            self.objID      = objID
    def getLoc():
        return self.centerLoc

    def getOrientation():
        return self.orientation

    def getObjID():
        return self.objID

class VWMTargetObj(VWMObj):
    def _init_(self):
        self.color = "red";
    def objType():
        print  "Target" 

class VWMDistractorObj(VWMObj):
    def _init_(self):
        self.color = "blue";
    def objType():
        print  "Distractor"         

# define trial class
class VWMTrial(object):    
    """trial properties for VWM alpha tACS """
    def __init__(self, arg):        
        self.trialID    = []
        self.condNum = [] # condition number: TODO define what each condition number is
        self.nTargets = [] # number of targets in the trial. these are associated with a specific color
        self.nDistractors = [] # number of distractors in the trial. these will be shown with a different color than the above. 


    def condition(self):


## Set number of conditions and 
TargetSets      = np.array([2,4])
DistractorSets  = np.array([0,2,4])
nConds = TargetSets.size*DistractorSets.size
nTrials = 720
nTrialsPerCond = nTrials/nConds


## set condition names and store
conds = {};
nTotalItemsPerCond = np.zeros(nConds)
cnt = 1;
for ts in range(TargetSets.size):
    for ds in range(DistractorSets.size):
        conds[cnt] = 'nT' + str(TargetSets[ts]) + 'nD' + str(DistractorSets[ds])
        nTotalItemsPerCond[cnt-1] = int(TargetSets[ts]+DistractorSets[ds])
        cnt += 1


# Set trial conditions and counter balance
TrialIDs = np.arange(nTrials)        # trial IDs
AvailableTrials = np.array(TrialIDs) 
TrialCondIDs   = np.zeros(nTrials)   # individual trial condition
ChangeTrialIDs = np.zeros(nTrials)   # test array changes at test
nTrialItems    = np.zeros(nTrials,int)   # total number of trials per item

for cond in range(nConds):
    trials = np.random.choice(AvailableTrials,nTrialsPerCond,replace=False)
    TrialCondIDs[trials] = cond+1
    AvailableTrials = np.setxor1d(AvailableTrials,trials)
    ChangeTrialIDs[np.random.choice(trials,nTrialsPerCond/2,replace=False)]=1
    nTrialItems[trials] = nTotalItemsPerCond[cond]
    
assert AvailableTrials.size==0, 'Error Assigning Trials'
hist=np.histogram(TrialCondIDs,range(1,nConds+2))[0]
assert sum(hist==nTrialsPerCond)==nConds, 'Uneven Trials'


# Set orientations and location for each item 
PossibleOrientations  = np.concatenate((np.arange(10,81),np.arange(100,171))); # in degrees
OrientTrialItems = {}
for tt in range(nTrials):
    OrientTrialItems[tt] = np.random.choice(PossibleOrientations,nTrialItems[tt])
        



