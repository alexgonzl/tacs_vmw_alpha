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

# calculates hit rate for each condition for (parameter) hem change trials
def hemHitRates(csv, hem):
    # read in csv file
    df = pd.read_csv(csv)

    # create boolean condition vectors of length nTrials
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    hemChanges = df['changeHemi'] == hem
    nTarg1 = df[hem + 'Targs'] == 1
    nTarg2 = df[hem + 'Targs'] == 2
    nDist0 = df[hem + 'Dists'] == 0
    nDist1 = df[hem + 'Dists'] == 1
    nDist2 = df[hem + 'Dists'] == 2

    # condition dictionary
    hemConds = OrderedDict([('t1d0', (nTarg1, nDist0)), ('t1d1', (nTarg1, nDist1)), ('t1d2', (nTarg1, nDist2)), ('t2d0', (nTarg2, nDist0)), ('t2d1', (nTarg2, nDist1)), ('t2d2', (nTarg2, nDist2))])
    hemHitRates = OrderedDict()

    # calculate hit rate
    for key in hemConds:
        hits = itemCounter(df, resps, hemChanges, hemConds[key][0], hemConds[key][1])
        misses = itemCounter(df, noResps, hemChanges, hemConds[key][0], hemConds[key][1])
        hitRate = hits/(hits+misses)
        hemHitRates[key] = hitRate
    return hemHitRates

# calculates dPrimes for each condition for (parameter) hem change trials
def hemdPrime(csv, hem):
    # read in csv file
    df = pd.read_csv(csv)

    # create boolean condition vectors of length nTrials
    oppositeHem = ''
    if hem == 'left':
        oppositeHem = 'right'
    else:
        oppositeHem == 'left'
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    hemChanges = df['changeHemi'] == hem
    noChanges = df['ChangeTrial'] == 0
    nTarg1 = df[hem + 'Targs'] == 1
    nTarg2 = df[hem + 'Targs'] == 2
    nDist0 = df[hem + 'Dists'] == 0
    nDist1 = df[hem + 'Dists'] == 1
    nDist2 = df[hem + 'Dists'] == 2

    # condition dictionary
    hemConds = OrderedDict([('t1d0', (nTarg1, nDist0)), ('t1d1', (nTarg1, nDist1)), ('t1d2', (nTarg1, nDist2)), ('t2d0', (nTarg2, nDist0)), ('t2d1', (nTarg2, nDist1)), ('t2d2', (nTarg2, nDist2))])
    hemdPrimes = OrderedDict()

    # calculate hit rate
    for key in hemConds:
        hits = itemCounter(df, resps, hemChanges, hemConds[key][0], hemConds[key][1])
        misses = itemCounter(df, noResps, hemChanges, hemConds[key][0], hemConds[key][1])
        falarms = itemCounter(df, resps, noChanges, hemConds[key][0], hemConds[key][1])
        crejects = itemCounter(df, noResps, noChanges, hemConds[key][0], hemConds[key][1])

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
        hemdPrimes[key]= Z(hitRate) - Z(faRate)

    return hemdPrimes
