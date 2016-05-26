from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging #, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
import random
import os  # handy system and path functions
import sys # to get file system encoding

from setup import VWMTrials, win
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

# Global Constants:
nTrials = len(VWMTrials)
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

def run(i):
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
    cnt = 0
    slideRects = []
    for rect in rectsPerTrial[i]:
        if VWMTrials[i].ChangeTrial == 1 and cnt == VWMTrials[i].ChangeTargID:
            rect.ori += VWMTrials[i].ChangeTargSign * rotation
            cnt += 1
        test_arrayComponents.append(rect)
        slideRects.append(rect)
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
    thisExp.addData('trialID', VWMTrials[i].trialID)
    thisExp.addData('Response key',testResponse.keys)
    if testResponse.keys != None:  # we had a response
        thisExp.addData('Response time', testResponse.rt)
    thisExp.addData('ChangeTrial', VWMTrials[i].ChangeTrial)
    thisExp.addData('nDistractors', VWMTrials[i].nDistractors)
    thisExp.addData('nTargets', VWMTrials[i].nTargets)
    thisExp.addData('condNum', VWMTrials[i].condNum)
    if VWMTrials[i].ChangeTrial == 1:
        thisExp.addData('changePos', slideRects[VWMTrials[i].ChangeTargID].pos)
    thisExp.nextEntry()

# Runs all 720 trials
for i in range(nTrials):
    run(i)

thisExp.saveAsExcel(filename, sheetName='expData', stimOut=None, dataOut=('n', 'all_mean', 'all_std', 'all_raw'), matrixOnly=False, appendFile=True, fileCollisionMethod='rename')
win.close()
core.quit()