# imports for setup
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
import numpy as np
from AppKit import NSScreen
from psychopy import visual, monitors, tools, data, core, event #, gui
from psychopy.tools import coordinatetools as coord
from psychopy.constants import *  # things like STARTED, FINISHED
import random
import os
import sys


# Constants
nTrials         = 368
# get monitor dimensions in pixels
MonitorWidth =  NSScreen.mainScreen().frame().size.width
MonitorHeight = NSScreen.mainScreen().frame().size.height

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'tacsVWMAlpha.py'
expInfo = {'participant':'', 'session':'001'}
## dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
## if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date']) + '.setup'

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name='setup_' + expName, version='', runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# set window
win = visual.Window(size=(MonitorWidth, MonitorHeight), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
                    monitor=mon, units = 'deg', color=[0,0,0], colorSpace='rgb', blendMode='avg')

# Targets and distractors sets
TargetSets      = np.array([2,4])
DistractorSets  = np.array([0,2,4])
# Set orientations and location for each item
PossibleObjOrientations  = np.concatenate((np.arange(10,81),np.arange(100,171)));
PossibleObjRadix         = np.array([2, 4])
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
nTrialsPerCond       = {1:44, 2:96, 3:44, 4:50, 5:84 ,6:50}
nSubCondsPerCond     = {1:4,2:16,3:4,4:1,5:4,6:1}
nTrialsPerSubCond    = {}
for cond in conds:
    nTrialsPerSubCond[cond] = nTrialsPerCond[cond]/nSubCondsPerCond[cond]

# sub-condition target/distractors pairings; note that these are all indexed/key by condition
CondsTargetQuadrants = {}
CondsDistraQuadrants = {}
quadTargDisOverlap   = {}

# Quadrant pairings and groupings for a trial
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
    quadOverlap = quadTargDisOverlap[cond][subCond]

    # bad code here. need to clean up #AG 4/26/16
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
    changeTargID = np.random.randint(VWMTrials[tt].nTargets, size=1)
    VWMTrials[tt].ChangeTargID = changeTargID[0]

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

# saves setup info
for i in range(nTrials):
    thisExp.addData('TrialID', TrialIDs[i])
    thisExp.addData('ChangeTrials', ChangeTrialIDs[i])
    thisExp.addData('TrialConds', TrialCondIDs[i])
    thisExp.addData('SubConds', TrialSubCondID[i])
    thisExp.nextEntry()

####### Run Method and Setup #######

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'tacsVWMAlpha.py'
expInfo = {'participant':'', 'session':'001'}
## dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
## if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

#TODO
actualChange = np.zeros(nTrials)

# Global Constants:
directionCueTime = 0.2
fixCrossTime = 0.1
stimArrayTime = 0.1
retentionTime = 1.0
testArrayTime = 1.0
itiTime = 0.6
rotation = 90

# Initialize fixation cross graphic
def makeCross():
    return visual.TextStim(win=win, ori=0,
    text=u'+',    font=u'Arial',
    pos=[0, 0], height=1.0, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "direct_cue"
direct_cueClock = core.Clock()
directionalCue = visual.TextStim(win=win, ori=0, name='text',
    text=u'\u2194',    font=u'Arial',
    pos=[0, 0], height=1.0, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "fix_cross"
fix_crossClock = core.Clock()
cross1 = makeCross()

# Initialize components for Routine "stim_array"
stim_arrayClock = core.Clock()
cross3 = makeCross()
rectsPerTrial = []
for trial in VWMTrials:
    trialObjsArray = trial.Objects
    rects = []
    for obj in trialObjsArray:
        rect = obj.rect
        rects.append(rect)
    rectsPerTrial.append(rects)

# Initialize components for Routine "reten_time"
reten_timeClock = core.Clock()
cross2 = makeCross()

# Initialize components for Routine "test_array"
test_arrayClock = core.Clock()
cross4 = makeCross()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# Initialize run method

def oneTrial(i):
#------Prepare to start Routine "direct_cue"-------
    t = 0 # time in seconds
    direct_cueClock.reset()  # clock
    routineTimer.add(directionCueTime)
    # update component parameters for each repeat
    # keep track of which components have finished
    directionalCue.status = NOT_STARTED

    #-------Start Routine "direct_cue"-------
    continueRoutine = True
    while routineTimer.getTime() > 0:
        # get current time for data saving
        t = direct_cueClock.getTime()
        # update/draw components on each frame

        # *directionalCue* updates
        if directionalCue.status == NOT_STARTED:
            # keep track of start time for later
            directionalCue.tStart = t  # underestimates by a little under one frame
            directionalCue.setAutoDraw(True)
        if directionalCue.status == STARTED and t >= (directionCueTime-win.monitorFramePeriod*0.75): #most of one frame period left
            directionalCue.setAutoDraw(False)
            continueRoutine = False

        if continueRoutine:
            win.flip() # refreshes the screen

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()

    #-------Ending Routine "direct_cue"-------
    directionalCue.setAutoDraw(False)

    #------Prepare to start Routine "fix_cross"-------
    t = 0
    fix_crossClock.reset()  # clock
    routineTimer.add(fixCrossTime)
    # update component parameters for each repeat
    # keep track of which components have finished
    cross1.status = NOT_STARTED

    #-------Start Routine "fix_cross"-------
    continueRoutine = True
    while routineTimer.getTime() > 0:
        # get current time
        t = fix_crossClock.getTime()
        # update/draw components on each frame

        # *cross1* updates
        if t >= 0.0 and cross1.status == NOT_STARTED:
            # keep track of start time for later
            cross1.tStart = t  # underestimates by a little under one frame
            cross1.setAutoDraw(True)
        if cross1.status == STARTED and t >= (fixCrossTime-win.monitorFramePeriod*0.75): #most of one frame period left
            cross1.setAutoDraw(False)
            continueRoutine = False

        if continueRoutine:
            win.flip() # refreshes the screen

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()

    #-------Ending Routine "fix_cross"-------
    cross1.setAutoDraw(False)

    #------Prepare to start Routine "stim_array"-------
    t = 0
    stim_arrayClock.reset()  # clock
    routineTimer.add(stimArrayTime)
    # update component parameters for each repeat
    # keep track of which components have finished
    stim_arrayComponents = []
    stim_arrayComponents.append(cross3)
    for rect in rectsPerTrial[i]:
        stim_arrayComponents.append(rect)
    for thisComponent in stim_arrayComponents:
        thisComponent.status = NOT_STARTED

    #-------Start Routine "stim_array"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = stim_arrayClock.getTime()
        # update/draw components on each frame

        # *cross3* updates
        if t >= 0.0 and cross3.status == NOT_STARTED:
            # keep track of start time for later
            cross3.tStart = t  # underestimates by a little under one frame
            cross3.setAutoDraw(True)
        if cross3.status == STARTED and t >= (stimArrayTime-win.monitorFramePeriod*0.75): #most of one frame period left
            cross3.setAutoDraw(False)

        # *Rects* updates
        for rect in rectsPerTrial[i]:
            if t >= 0.0 and rect.status == NOT_STARTED:
                # keep track of start time for later
                rect.tStart = t  # underestimates by a little under one frame
                rect.setAutoDraw(True)

        if t >= (0.0 + (stimArrayTime-win.monitorFramePeriod*0.75)): #most of one frame period left
            for rect in rectsPerTrial[i]:
                rect.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in stim_arrayComponents:
            if thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "stim_array"-------
    for thisComponent in stim_arrayComponents:
        thisComponent.setAutoDraw(False)

    #------Prepare to start Routine "reten_time"-------
    t = 0
    reten_timeClock.reset()  # clock
    routineTimer.add(retentionTime)
    # update component parameters for each repeat
    # keep track of which components have finished
    cross2.status = NOT_STARTED

    #-------Start Routine "reten_time"-------
    continueRoutine = True
    while routineTimer.getTime() > 0:
        # get current time
        t = reten_timeClock.getTime()
        # update/draw components on each frame

        # *cross2* updates
        if t >= 0.0 and cross2.status == NOT_STARTED:
            # keep track of start time for later
            cross2.tStart = t  # underestimates by a little under one frame
            cross2.setAutoDraw(True)
        if cross2.status == STARTED and t >= (retentionTime-win.monitorFramePeriod*0.75): #most of one frame period left
            cross2.setAutoDraw(False)
            continueRoutine = False

        if continueRoutine:
            win.flip() # refreshes the screen

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()

    #-------Ending Routine "reten_time"-------
    cross2.setAutoDraw(False)

    #------Prepare to start Routine "test_array"-------
    t = 0
    test_arrayClock.reset()  # clock
    routineTimer.add(testArrayTime + itiTime)
    # update component parameters for each repeat
    testResponse = event.BuilderKeyResponse()  # create an object of type KeyResponse
    testResponse.status = NOT_STARTED
    # keep track of which components have finished
    test_arrayComponents = []
    test_arrayComponents.append(testResponse)
    test_arrayComponents.append(cross4)
    slideRects = []
    for rect in rectsPerTrial[i]:
        test_arrayComponents.append(rect)
        slideRects.append(rect)
    if VWMTrials[i].ChangeTrial == 1:
        slideRects[VWMTrials[i].ChangeTargID].ori += VWMTrials[i].ChangeTargSign * rotation
        actualChange[i] = 1 ##TODO
    for thisComponent in test_arrayComponents:
        thisComponent.status = NOT_STARTED

    #-------Start Routine "test_array"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        endExpNow = False
        # get current time
        t = test_arrayClock.getTime()
        # update/draw components on each frame

        # *Rects* updates
        for rect in slideRects:
            if t >= 0.0 and rect.status == NOT_STARTED:
                # keep track of start time for later
                rect.tStart = t  # underestimates by a little under one frame
                rect.setAutoDraw(True)

        if t >= (0.0 + (testArrayTime-win.monitorFramePeriod*0.75)): #most of one frame period left
            for rect in rectsPerTrial[i]:
                rect.setAutoDraw(False)

        # *cross4* updates
        if t >= 0.0 and cross4.status == NOT_STARTED:
            # keep track of start time for later
            cross4.tStart = t  # underestimates by a little under one frame
            cross4.setAutoDraw(True)
        if cross4.status == STARTED and t >= (testArrayTime - win.monitorFramePeriod*0.75): #most of one frame period left
            cross4.setAutoDraw(False)

        # *testResponse* updates
        if t >= 0.0 and testResponse.status == NOT_STARTED:
            # keep track of start time for later
            testResponse.tStart = t  # underestimates by a little under one frame
            testResponse.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(testResponse.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if testResponse.status == STARTED and t >= (testArrayTime + itiTime -win.monitorFramePeriod*0.75): #most of one frame period left
            testResponse.status = STOPPED
        if testResponse.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                testResponse.keys = theseKeys[-1]  # just the last key pressed
                testResponse.rt = testResponse.clock.getTime()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in test_arrayComponents:
            if thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "test_array"-------
    for thisComponent in test_arrayComponents:
        if hasattr(thisComponent, 'setAutoDraw'):
            thisComponent.setAutoDraw(False)
    # check responses
    if testResponse.keys in ['', [], None]:  # No response was made
       testResponse.keys=None
    # store data for thisExp (ExperimentHandler)
    resp = 0
    if testResponse.keys == 'space':
        resp = 1
    thisExp.addData('trialID', VWMTrials[i].trialID)
    thisExp.addData('Response',resp)
    if testResponse.keys != None:  # we had a response
        thisExp.addData('RT', testResponse.rt)
    thisExp.addData('ChangeTrial', VWMTrials[i].ChangeTrial)
    thisExp.addData('ActualChange', actualChange[i])
    thisExp.addData('ChangeTargID', VWMTrials[i].ChangeTargID)
    thisExp.addData('nDistractors', VWMTrials[i].nDistractors)
    thisExp.addData('nTargets', VWMTrials[i].nTargets)
    thisExp.addData('condNum', VWMTrials[i].condNum)
    if VWMTrials[i].ChangeTrial == 1:
        thisExp.addData('changePos', slideRects[VWMTrials[i].ChangeTargID].pos)
    thisExp.nextEntry()
