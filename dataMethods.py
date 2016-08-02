from __future__ import division
import pandas as pd
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
from collections import OrderedDict
from scipy.stats import norm
Z = norm.ppf

# counts number of trials corresponding to inputted conditions
def condCounter(df, responseType, changeType, cond):
    count = float(len(df[responseType & changeType & cond]))
    return count

# calculates K pased on Pashler equation: K = S * ((H - F) / (1 - F))
def kCalculation(s, h, f):
    k = s * ((h - f) / (1 - f))
    return k

# calculates pashler K for each condition from csv data file
def pashlerK(csv, hem):
    # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    changeNum = 0
    if hem == 'left':
        changeNum = 1
    elif hem == 'right':
        changeNum = 2
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    changes = 0
    noChanges = 0
    if changeNum == 0:
        changes = df['ChangeTrial'] == 1
        noChanges = df['ChangeTrial'] == 0
    else:
        changes = df['ChangeCond'] == changeNum
        noChanges = df['ChangeCond'] != changeNum
    t1d0 = df['WFCond'] == 1
    t1d1 = df['WFCond'] == 2
    t1d2 = df['WFCond'] == 3
    t2d0 = df['WFCond'] == 4
    t2d1 = df['WFCond'] == 5
    t2d2 = df['WFCond'] == 6

    # initialize dictionaries
    hitRates = OrderedDict()
    fAlarmRates = OrderedDict()
    Kvals = OrderedDict()
    HFconds = OrderedDict([('t1d0', t1d0), ('t1d1', t1d1), ('t1d2', t1d2), ('t2d0', t2d0), ('t2d1', t2d1), ('t2d2', t2d2)])

    # store rate values
    for key in HFconds:
        hits = condCounter(df, resps, changes, HFconds[key])
        misses = condCounter(df, noResps, changes, HFconds[key])
        falarms = condCounter(df, resps, noChanges, HFconds[key])
        crejects = condCounter(df, noResps, noChanges, HFconds[key])
        hitRates[key] = hits/(hits+misses)
        fAlarmRates[key] = falarms/(falarms+crejects)
        s = 0
        if key == 't1d0' or key == 't1d1' or key == 't1d2':
            s = 1
        else:
            s = 2
        Kvals[key] = kCalculation(s, hitRates[key], fAlarmRates[key])
    return {'Kvals': Kvals, 'hitRates': hitRates, 'fAlarmRates': fAlarmRates}


# calculates mean RT for each condition from csv data file
def rtCalc(csv, hem):
    # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    resps = df['Response'] == 1
    changes = 0
    if hem != 'left' or hem != 'right':
        changes = df['ChangeTrial'] == 1
    else:
        changes = df['changeHemi'] == hem
    t1d0 = df['WFCond'] == 1
    t1d1 = df['WFCond'] == 2
    t1d2 = df['WFCond'] == 3
    t2d0 = df['WFCond'] == 4
    t2d1 = df['WFCond'] == 5
    t2d2 = df['WFCond'] == 6

    # initialize dictionary
    rtRates = OrderedDict()
    HFconds = OrderedDict([('t1d0', t1d0), ('t1d1', t1d1), ('t1d2', t1d2), ('t2d0', t2d0), ('t2d1', t2d1), ('t2d2', t2d2)])

    # calculate average RT value
    for key in HFconds:
        rows = df[HFconds[key] & resps & changes]
        rts = rows['RT']
        meanRT = rts.mean()
        rtRates[key] = meanRT
    return rtRates


# calculates d's for each condition from csv data file
def dprime(csv, hem):
     # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    changeNum = 0
    if hem == 'left':
        changeNum = 1
    elif hem == 'right':
        changeNum = 2
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    changes = 0
    noChanges = 0
    if changeNum == 0:
        changes = df['ChangeTrial'] == 1
        noChanges = df['ChangeTrial'] == 0
    else:
        changes = df['ChangeCond'] == changeNum
        noChanges = df['ChangeCond'] != changeNum
    t1d0 = df['WFCond'] == 1
    t1d1 = df['WFCond'] == 2
    t1d2 = df['WFCond'] == 3
    t2d0 = df['WFCond'] == 4
    t2d1 = df['WFCond'] == 5
    t2d2 = df['WFCond'] == 6

    # initialize dict
    dprimes = OrderedDict()
    HFconds = OrderedDict([('t1d0', t1d0), ('t1d1', t1d1), ('t1d2', t1d2), ('t2d0', t2d0), ('t2d1', t2d1), ('t2d2', t2d2)])

    # calculate d-primes for each condition
    for key in HFconds:
        hits = condCounter(df, resps, changes, HFconds[key])
        misses = condCounter(df, noResps, changes, HFconds[key])
        falarms = condCounter(df, resps, noChanges, HFconds[key])
        crejects = condCounter(df, noResps, noChanges, HFconds[key])

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
