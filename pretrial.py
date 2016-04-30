from psychopy import visual, core, data, event, logging
from psychopy.constants import *  # things like STARTED, FINISHED
from setup import VWMTrials, win

# Initialize routine timer
routineTimer = core.Clock()

# Initialize Instruction text
instructions = visual.TextStim(win=win, ori=0, name='instr',
    text="Please look at the fixation cross during the course of the study. Pay attention only to the red rectangles, as the blue rectangles are distractors. You will be presented with two (nearly) identical displays of rectangles for each trial-- sometimes one of the red rectangles will rotate 45 deg between the two presentations. If you think a rotation occured, press the space bar. Now press any key to continue", 
    font=u'Arial', pos=[0,0], height=0.1, wrapWidth=None, 
    color=u'white', colorSpace='rgb',
    opacity=1, depth=0.0)

# Initialize Practice round text
practiceText = visual.TextStim(win=win, ori=0, name='instr',
    text="This is a practice round. Make sure to press the spacebar immediately after the second slide is presented if you think a change has occured. Press any key to continue.", 
    font=u'Arial',
    pos=[0,0], height=0.1, wrapWidth=None, color=u'white', colorSpace='rgb',
    opacity=1, depth=0.0)
finalText = visual.TextStim(win=win, ori=0, name='instr',
    text="Press any key to practice again. Press escape to exit", 
    font=u'Arial',
    pos=[0,0], height=0.1, wrapWidth=None, color=u'white', colorSpace='rgb',
    opacity=1, depth=0.0)

# Global Constants:
nTrials = 720
directionCueTime = 0.2
fixCrossTime = 0.1
stimArrayTime = 0.1
retentionTime = 1.0
testArrayTime = 1.0
itiTime = 0.6

# Initialize fixation cross graphic
def makeCross():
    return visual.TextStim(win=win, ori=0,
    text=u'+',    font=u'Arial',
    pos=[0, 0], height=0.2, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "direct_cue"
direct_cueClock = core.Clock()
directionalCue = visual.TextStim(win=win, ori=0, name='text',
    text=u'\u2194',    font=u'Arial',
    pos=[0, 0], height=0.2, wrapWidth=None,
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
            rect.ori += 45.0
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
                # a response ends the routine
                continueRoutine = False                 
                         
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


# Presents Instructions
while(True):
    instructions.setAutoDraw(True)
    win.flip()
    if len(event.getKeys()) > 0:
        break
instructions.setAutoDraw(False)

# Runs practice rounds
cnt = 0
while(True):
    routineTimer.add(5)
    while (routineTimer.getTime > 0):
        practiceText.setAutoDraw(True)
        win.flip()
        if len(event.getKeys()) > 0:
            break
    practiceText.setAutoDraw(False)
    run(cnt)
    while(True):
        finalText.setAutoDraw(True)
        win.flip()
        if len(event.getKeys(keyList=['escape'])) > 0:
            win.close()
            core.quit()
        if len(event.getKeys()) > 0:
            break
    finalText.setAutoDraw(False)
    cnt += 1