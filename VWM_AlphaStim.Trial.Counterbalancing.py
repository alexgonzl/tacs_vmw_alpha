import numpy as np


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
        



