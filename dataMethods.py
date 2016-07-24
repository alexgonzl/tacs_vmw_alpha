from __future__ import division
import pandas as pd
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
from collections import OrderedDict
from scipy.stats import norm
Z = norm.ppf

# counts number of trials corresponding to inputted conditions
def itemCounter(df, responseType, changeType, t, d):
    count = float(len(df[responseType & changeType & t & d]))
    return count

# calculates K pased on Pashler equation: K = S * ((H - F) / (1 - F))
def kCalculation(s, h, f):
    k = s * ((h - f) / (1 - f))
    return k

# calculates pashler K for each condition from csv data file
def pashlerK(csv):
    # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    changes = df['ChangeTrial'] == 1
    noChanges = df['ChangeTrial'] == 0
    targ2 = df['nTargets'] == 2
    targ4 = df['nTargets'] == 4
    dist0 = df['nDistractors'] == 0
    dist2 = df['nDistractors'] == 2
    dist4 = df['nDistractors'] == 4

    # initialize dictionaries
    hitRates = OrderedDict()
    fAlarmRates = OrderedDict()
    Kvals = OrderedDict()

    conds = OrderedDict([('t2d0', (targ2, dist0)), ('t2d2', (targ2, dist2)), ('t2d4', (targ2, dist4)), ('t4d0', (targ4, dist0)), ('t4d2', (targ4, dist2)), ('t4d4', (targ4, dist4))])

    # store rate values
    for key in conds:
        hits = itemCounter(df, resps, changes, conds[key][0], conds[key][1])
        misses = itemCounter(df, noResps, changes, conds[key][0], conds[key][1])
        falarms = itemCounter(df, resps, noChanges, conds[key][0], conds[key][1])
        crejects = itemCounter(df, noResps, noChanges, conds[key][0], conds[key][1])
        hitRates[key] = hits/(hits+misses)
        fAlarmRates[key] = falarms/(falarms+crejects)
        s = 0
        if key == 't2d0' or key == 't2d2' or key == 't2d4':
            s = 2
        else:
            s = 4
        Kvals[key] = kCalculation(s, hitRates[key], fAlarmRates[key])
    return {'Kvals': Kvals, 'hitRates': hitRates, 'fAlarmRates': fAlarmRates}


# calculates mean RT for each condition from csv data file
def rtCalc(csv):
    # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    resps = df['Response'] == 1
    targ2 = df['nTargets'] == 2
    targ4 = df['nTargets'] == 4
    dist0 = df['nDistractors'] == 0
    dist2 = df['nDistractors'] == 2
    dist4 = df['nDistractors'] == 4

    # initialize dictionary
    rtRates = OrderedDict()
    conds = OrderedDict([('t2d0', (targ2, dist0)), ('t2d2', (targ2, dist2)), ('t2d4', (targ2, dist4)), ('t4d0', (targ4, dist0)), ('t4d2', (targ4, dist2)), ('t4d4', (targ4, dist4))])

    # calculate average RT value
    for key in conds:
        rows = df[conds[key][0] & conds[key][1] & resps]
        rts = rows['RT']
        meanRT = rts.mean()
        rtRates[key] = meanRT
    return rtRates


# calculates d's for each condition from csv data file
def dprime(csv):
     # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    changes = df['ChangeTrial'] == 1
    noChanges = df['ChangeTrial'] == 0
    targ2 = df['nTargets'] == 2
    targ4 = df['nTargets'] == 4
    dist0 = df['nDistractors'] == 0
    dist2 = df['nDistractors'] == 2
    dist4 = df['nDistractors'] == 4

    # initialize dict
    hits = OrderedDict()
    misses = OrderedDict()
    falarms = OrderedDict()
    crejects = OrderedDict()
    dprimes = OrderedDict()

    conds = OrderedDict([('t2d0', (targ2, dist0)), ('t2d2', (targ2, dist2)), ('t2d4', (targ2, dist4)), ('t4d0', (targ4, dist0)), ('t4d2', (targ4, dist2)), ('t4d4', (targ4, dist4))])

    # calculate d-primes for each condition
    for key in conds:
        hits = itemCounter(df, resps, changes, conds[key][0], conds[key][1])
        misses = itemCounter(df, noResps, changes, conds[key][0], conds[key][1])
        falarms = itemCounter(df, resps, noChanges, conds[key][0], conds[key][1])
        crejects = itemCounter(df, noResps, noChanges, conds[key][0], conds[key][1])

        # Floors an ceilings are replaced by half hits and half FA's
        halfHit = 0.5/(hits+misses)
        halfFa = 0.5/(falarms+crejects)

        # Calculate hitrate and avoid d' infinity
        hitRate = hits/(hits+misses)
        if hitRate == 1: hitRate = 1-halfHit
        if hitRate == 0: hitRate = halfHit

        # Calculate false alarm rate and avoid d' infinity
        faRate = falarms/(falarms+crejects)
        if faRate == 1: faRate = 1-halfFa
        if faRate == 0: faRate = halfFa

        # calculate dprime using Z (ppf function in scipy.norm)
        dprimes[key]= Z(hitRate) - Z(faRate)

    return dprimes

# calculates hit rate for each condition for left hem change trials
def leftHemHitRates(csv):
    # read in csv file
    df = pd.read_csv(csv)

    # create boolean condition vectors of length nTrials
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    leftChanges = df['changeHemi'] == 'left'
    nLeftTarg1 = df['leftTargs'] == 1
    nLeftTarg2 = df['leftTargs'] == 2
    nLeftDist0 = df['leftDists'] == 0
    nLeftDist1 = df['leftDists'] == 1
    nLeftDist2 = df['leftDists'] == 2

    # condition dictionary
    leftConds = OrderedDict([('t1d0', (nLeftTarg1, nLeftDist0)), ('t1d1', (nLeftTarg1, nLeftDist1)), ('t1d2', (nLeftTarg1, nLeftDist2)), ('t2d0', (nLeftTarg2, nLeftDist0)), ('t2d1', (nLeftTarg2, nLeftDist1)), ('t2d2', (nLeftTarg2, nLeftDist2))])
    leftHitRates = OrderedDict()

    # calculate hit rate
    for key in leftConds:
        hits = itemCounter(df, resps, leftChanges, leftConds[key][0], leftConds[key][1])
        misses = itemCounter(df, noResps, leftChanges, leftConds[key][0], leftConds[key][1])
        hitRate = hits/(hits+misses)
        leftHitRates[key] = hitRate
    return leftHitRates


# calculates hit rate for each condition for right hem change trials
def rightHemHitRates(csv):
    # read in csv file
    df = pd.read_csv(csv)

    # create boolean condition vectors of length nTrials
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    rightChanges = df['changeHemi'] == 'right'
    nRightTarg1 = df['rightTargs'] == 1
    nRightTarg2 = df['rightTargs'] == 2
    nRightDist0 = df['rightDists'] == 0
    nRightDist1 = df['rightDists'] == 1
    nRightDist2 = df['rightDists'] == 2

    # condition dictionary
    rightConds = OrderedDict([('t1d0', (nRightTarg1, nRightDist0)), ('t1d1', (nRightTarg1, nRightDist1)), ('t1d2', (nRightTarg1, nRightDist2)), ('t2d0', (nRightTarg2, nRightDist0)), ('t2d1', (nRightTarg2, nRightDist1)), ('t2d2', (nRightTarg2, nRightDist2))])
    rightHitRates = OrderedDict()

    # calculate hit rate
    for key in rightConds:
        hits = itemCounter(df, resps, rightChanges, rightConds[key][0], rightConds[key][1])
        misses = itemCounter(df, noResps, rightChanges, rightConds[key][0], rightConds[key][1])
        hitRate = hits/(hits+misses)
        rightHitRates[key] = hitRate
    return rightHitRates
