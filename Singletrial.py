from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys # to get file system encoding

from vwmSetup import trials

# Start Code - component code to be run before the window creation
win = visual.Window(size=(1280, 800), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )

# Initialize fixation cross graphic
def makeCross():
    return visual.TextStim(win=win, ori=0, name=NONE,
    text=u'+',    font=u'Arial',
    pos=[0, 0], height=0.2, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "direct_cue"
direct_cueClock = core.Clock()
directionalCue = visual.TextStim(win=win, ori=0, name='text',
    text=u'\u2194',    font=u'Arial',
    pos=[0, 0], height=0.3, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "fix_cross"
fix_crossClock = core.Clock()
cross1 = makeCross()

# Initialize components for Routine "stim_array"
stim_arrayClock = core.Clock()
timer = visual.TextStim(win=win, ori=0, name='timer',
    text=None,    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)
cross3 = makeCross()

# Initialize components for Routine "reten_time"
reten_timeClock = core.Clock()
cross2 = makeCross()

# Initialize components for Routine "test_array"
test_arrayClock = core.Clock()
cross4 = makeCross()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
#### *TODO* Why two routine timers? #######

for i in range(1):

#------Prepare to start Routine "direct_cue"-------
    t = 0 # time in seconds
    direct_cueClock.reset()  # clock 
    routineTimer.add(0.200000)
    # update component parameters for each repeat
    # keep track of which components have finished
    direct_cueComponents = []
    direct_cueComponents.append(directionalCue)
    directionalCue.status = NOT_STARTED
    
    #-------Start Routine "direct_cue"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0: ### *TODO* Can get rid of while loop and multiple win flips ####
        # get current time
        t = direct_cueClock.getTime()
        # update/draw components on each frame
        
        # *text* updates
        if directionalCue.status == NOT_STARTED:
            # keep track of start time for later
            directionalCue.tStart = t  # underestimates by a little under one frame
            directionalCue.setAutoDraw(True)
        if directionalCue.status == STARTED and t >= (0.2-win.monitorFramePeriod*0.75): #most of one frame period left
            directionalCue.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        if directionalCue.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "direct_cue"-------
    for thisComponent in direct_cueComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #------Prepare to start Routine "fix_cross"-------
    t = 0
    fix_crossClock.reset()  # clock
    routineTimer.add(0.100000)
    # update component parameters for each repeat
    # keep track of which components have finished
    fix_crossComponents = []
    fix_crossComponents.append(cross1)
    for thisComponent in fix_crossComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "fix_cross"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = fix_crossClock.getTime()
        # update/draw components on each frame
        
        # *cross1* updates
        if t >= 0.0 and cross1.status == NOT_STARTED:
            # keep track of start time for later
            cross1.tStart = t  # underestimates by a little under one frame
            cross1.setAutoDraw(True)
        if cross1.status == STARTED and t >= (0.0 + (.1-win.monitorFramePeriod*0.75)): #most of one frame period left
            cross1.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fix_crossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "fix_cross"-------
    for thisComponent in fix_crossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #------Prepare to start Routine "stim_array"-------
    t = 0
    stim_arrayClock.reset()  # clock
    routineTimer.add(0.100000)
    # update component parameters for each repeat
    # keep track of which components have finished
    stim_arrayComponents = [] #### *TODO* make array of stim_arrayComponents at the top
    stim_arrayComponents.append(cross3)
    targetRects = trials.VWMTrials[0].TargetObjs
    distractorRects = trials.VWMTrials[0].Distrators
    for targetObj in targetRects:
        stim_arrayComponents.append(targetObj)
    for distractor in distractorRects:
        stim_arrayComponents.append(distractor)
    for thisComponent in stim_arrayComponents:
        if hasattr(thisComponent, 'status'):
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
        if cross3.status == STARTED and t >= (0.0 + (.1-win.monitorFramePeriod*0.75)): #most of one frame period left
            cross3.setAutoDraw(False)

        # *targetRects* updates
        for j in targetRects:
            if t >= 0.0 and targetRects[j].status == NOT_STARTED:
                # keep track of start time for later
                targetRects[j].tStart = t  # underestimates by a little under one frame
                targetRects[j].setAutoDraw(True)
        
        if t >= (0.0 + (.1-win.monitorFramePeriod*0.75)): #most of one frame period left
            for jj in targetRects:
                targetRects[jj].setAutoDraw(False)
        
        # *distractorRects* updates
        for j in distractorRects:
            if t >= 0.0 and distractorRects[j].status == NOT_STARTED:
                # keep track of start time for later
                distractorRects[j].tStart = t  # underestimates by a little under one frame
                distractorRects[j].setAutoDraw(True)
        
        if t >= (0.0 + (.1-win.monitorFramePeriod*0.75)): #most of one frame period left
            for jj in distractorRects:
                distractorRects[jj].setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in stim_arrayComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "stim_array"-------
    for thisComponent in stim_arrayComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #------Prepare to start Routine "reten_time"-------
    t = 0
    reten_timeClock.reset()  # clock
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    reten_timeComponents = []
    reten_timeComponents.append(cross2)
    for thisComponent in reten_timeComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "reten_time"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = reten_timeClock.getTime()
        # update/draw components on each frame
        
        # *cross2* updates
        if t >= 0.0 and cross2.status == NOT_STARTED:
            # keep track of start time for later
            cross2.tStart = t  # underestimates by a little under one frame
            cross2.setAutoDraw(True)
        if cross2.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            cross2.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in reten_timeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "reten_time"-------
    for thisComponent in reten_timeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #------Prepare to start Routine "test_array"-------
    t = 0
    test_arrayClock.reset()  # clock
    routineTimer.add(1.600000)
    # update component parameters for each repeat
    testResponse = event.BuilderKeyResponse()  # create an object of type KeyResponse
    testResponse.status = NOT_STARTED
    # keep track of which components have finished
    test_arrayComponents = [] ## *TODO* make array of test_arrayComponents
    test_arrayComponents.append(testResponse)
    test_arrayComponents.append(cross4)
    if (trials.ChangeTrialIDs[0] == 1):
        targetRects[0].ori += 90 ## *TODO* set orientations in data structure of this program ##
    for targetObj in targetRects:
        test_arrayComponents.append(targetObj)
    for distractor in distractorRects:
        test_arrayComponents.append(distractor)
    test_arrayComponents.append(trialRectArrays[i])
    ############################################################ Add line to record prescence of change trial
    for thisComponent in test_arrayComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "test_array"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = test_arrayClock.getTime()
        # update/draw components on each frame
        
        # *targetRects* updates
        for j in targetRects:
            if t >= 0.0 and targetRects[j].status == NOT_STARTED:
                # keep track of start time for later
                targetRects[j].tStart = t  # underestimates by a little under one frame
                targetRects[j].setAutoDraw(True)
        
        if t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            for jj in targetRects:
                targetRects[jj].setAutoDraw(False)
        
        # *distractorRects* updates
        for j in distractorRects:
            if t >= 0.0 and distractorRects[j].status == NOT_STARTED:
                # keep track of start time for later
                distractorRects[j].tStart = t  # underestimates by a little under one frame
                distractorRects[j].setAutoDraw(True)
        
        if t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            for jj in distractorRects:
                distractorRects[jj].setAutoDraw(False)              
        
        # *cross4* updates
        if t >= 0.0 and cross4.status == NOT_STARTED:
            # keep track of start time for later
            cross4.tStart = t  # underestimates by a little under one frame
            cross4.setAutoDraw(True)
        if cross4.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            cross4.setAutoDraw(False)

        # *testResponse* updates
        if t >= 0.0 and testResponse.status == NOT_STARTED:
            # keep track of start time for later
            testResponse.tStart = t  # underestimates by a little under one frame
            testResponse.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(testResponse.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if testResponse.status == STARTED and t >= (0.0 + (1.6-win.monitorFramePeriod*0.75)): #most of one frame period left
            testResponse.status = STOPPED
        if testResponse.status == STARTED:
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                testResponse.keys = theseKeys[-1]  # just the last key pressed
                testResponse.rt = testResponse.clock.getTime()
                # a response ends the routine
                continueRoutine = False                 
                         
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in test_arrayComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
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
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if testResponse.keys in ['', [], None]:  # No response was made
       testResponse.keys=None
    # store data for trials (TrialHandler)
    trialData.addData('testResponse.keys',testResponse.keys)
    if testResponse.keys != None:  # we had a response
        trialData.addData('testResponse.rt', testResponse.rt)
    thisExp.nextEntry()

win.close()
core.quit()