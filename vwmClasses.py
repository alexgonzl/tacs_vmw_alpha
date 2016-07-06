import numpy as np

# Targets and distractors sets
TargetSets      = np.array([2,4])
DistractorSets  = np.array([0,2,4])

# number of conditions dependent on # of targets and distractors
nConds = TargetSets.size*DistractorSets.size

######### Assign Condition Names ###############
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

###  Visual Working Memory Object Class
class VWMObj():
    """ Trial objects. """
    size = (.5, 1.5)
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
        self.hemifield      = 'none'

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

    def getHemifield(self):
        return self.hemifield

    def setOrientation(self, o):
        self.orientation = o

    def setLoc(self, p):
        self.centerLoc = p
        if self.centerLoc[0] < 0:
            self.hemifield = 'left'
        else:
            self.hemifield = 'right'

###  Visual Working Memory Trial Class
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
        self.Objects        = []
        self.ObjTarg        = np.zeros(self.nTotalItems,np.int)
        self.rotation       = 0
        cnt = 0
        for obj in range(self.nTargets):
            self.Objects.append(VWMObj('target',cnt))
            self.ObjTarg[cnt]=1
            cnt+=1
        for obj in range(self.nDistractors):
            self.Objects.append(VWMObj('distractor',cnt))
            self.ObjTarg[cnt]=0
            cnt+=1
