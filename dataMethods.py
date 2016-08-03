from __future__ import division
import pandas as pd
from collections import OrderedDict
from scipy.stats import norm
Z = norm.ppf
import os
from os.path import expanduser
import re

# establish file data directory
homeDirectory = expanduser("~")
dataDirectory = homeDirectory + os.sep + 'Google Drive/tACS_VWM_ALPHA/data/stim1/'

# counts number of trials corresponding to inputted conditions
def condCounter(df, responseType, changeType, cond):
    count = float(len(df[responseType & changeType & cond]))
    return count

# calculates K pased on Pashler equation: K = S * ((H - F) / (1 - F))
def pashlerK(hits, misses, falarms, crejects, cond):
    S = cond[1]
    hitRate = hits/(hits+misses)
    faRate = falarms/(falarms+crejects)
    K = int(S) * ((hitRate - faRate) / (1 - faRate))
    return {'K': K, 'hitRate': hitRate, 'faRate': faRate}

# calculates d's using Z from scipy.stats.norm.ppf()
def dprime(hits, misses, falarms, crejects):

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
    dprime = Z(hitRate) - Z(faRate)

    return dprime

def extractPerformance(subj, run):
    # read in csv file
    saveDirectory = dataDirectory + 's' + str(subj) + os.sep + 'runData/'
    directoryFiles = os.listdir(saveDirectory)
    csv = ''
    for file in directoryFiles:
        match = re.match('run' + str(run) + '.*', file, re.M|re.I)
        if match != None:
            csv = saveDirectory + match.group()
    df = pd.read_csv(csv)

    # create conditions
    resps = df['Response'] == 1
    noResps = df['Response'] == 0
    changes = df['ChangeTrial'] == 1
    noChanges = df['ChangeTrial'] == 0
    lChanges = df['ChangeCond'] == 1
    lNoChanges = df['ChangeCond'] != 1
    rChanges = df['ChangeCond'] == 2
    rNoChanges = df['ChangeCond'] != 2
    t1d0 = df['WFCond'] == 1
    t1d1 = df['WFCond'] == 2
    t1d2 = df['WFCond'] == 3
    t2d0 = df['WFCond'] == 4
    t2d1 = df['WFCond'] == 5
    t2d2 = df['WFCond'] == 6

    # initialize dictionaries
    lHits = OrderedDict()
    lMisses = OrderedDict()
    lFAs = OrderedDict()
    lCRs = OrderedDict()
    rHits = OrderedDict()
    rMisses = OrderedDict()
    rFAs = OrderedDict()
    rCRs = OrderedDict()
    wHits = OrderedDict()
    wMisses = OrderedDict()
    wFAs = OrderedDict()
    wCRs = OrderedDict()
    lHitRTs = OrderedDict()
    rHitRTs = OrderedDict()
    lFaRTs = OrderedDict()
    rFaRTs = OrderedDict()
    lKs = OrderedDict()
    rKs = OrderedDict()
    lHRs = OrderedDict()
    rHRs = OrderedDict()
    ldPs = OrderedDict()
    rdPs = OrderedDict()
    wHRs = OrderedDict()
    wKs = OrderedDict()
    wHitRTs = OrderedDict()
    wFaRTs = OrderedDict()
    wdPs = OrderedDict()
    HFconds = OrderedDict([('t1d0', t1d0), ('t1d1', t1d1), ('t1d2', t1d2), ('t2d0', t2d0), ('t2d1', t2d1), ('t2d2', t2d2)])

    # store rate values
    for key in HFconds:
        lHits[key] = condCounter(df, resps, lChanges, HFconds[key])
        lMisses[key] = condCounter(df, noResps, lChanges, HFconds[key])
        lFAs[key] = condCounter(df, resps, lNoChanges, HFconds[key])
        lCRs[key] = condCounter(df, noResps, lNoChanges, HFconds[key])
        rHits[key] = condCounter(df, resps, rChanges, HFconds[key])
        rMisses[key] = condCounter(df, noResps, rChanges, HFconds[key])
        rFAs[key] = condCounter(df, resps, rNoChanges, HFconds[key])
        rCRs[key] = condCounter(df, noResps, rNoChanges, HFconds[key])
        wHits[key] = condCounter(df, resps, changes, HFconds[key])
        wMisses[key] = condCounter(df, noResps, changes, HFconds[key])
        wFAs[key] = condCounter(df, resps, noChanges, HFconds[key])
        wCRs[key] = condCounter(df, noResps, noChanges, HFconds[key])
        lHitRows = df[HFconds[key] & resps & lChanges]
        rHitRows = df[HFconds[key] & resps & rChanges]
        lFalarmRows = df[HFconds[key] & resps & lNoChanges]
        rFalarmRows = df[HFconds[key] & resps & rNoChanges]
        lHitRTs[key] = lHitRows['RT'].median()
        rHitRTs[key] = rHitRows['RT'].median()
        lFaRTs[key] = lFalarmRows['RT'].median()
        rFaRTs[key] = rFalarmRows['RT'].median()
        lHRs[key] = pashlerK(lHits[key],lMisses[key],lFAs[key], lCRs[key], key)['hitRate']
        rHRs[key] = pashlerK(rHits[key],rMisses[key],rFAs[key], rCRs[key], key)['hitRate']
        lKs[key] = pashlerK(lHits[key],lMisses[key],lFAs[key], lCRs[key], key)['K']
        rKs[key] = pashlerK(rHits[key],rMisses[key],rFAs[key], rCRs[key], key)['K']
        ldPs[key] = dprime(lHits[key],lMisses[key],lFAs[key], lCRs[key])
        rdPs[key] = dprime(rHits[key],rMisses[key],rFAs[key], rCRs[key])
        wHRs[key] = pashlerK(wHits[key],wMisses[key],wFAs[key], wCRs[key], key)['hitRate']
        wKs[key] = pashlerK(wHits[key],wMisses[key],wFAs[key], wCRs[key], key)['K']
        wHitRows = df[HFconds[key] & resps & changes]
        wFalarmRows = df[HFconds[key] & resps & noChanges]
        wHitRTs[key] = wHitRows['RT'].median()
        wFaRTs[key] = wFalarmRows['RT'].median()
        wdPs[key] = dprime(wHits[key],wMisses[key],wFAs[key], wCRs[key])

    return {'lHits': lHits, 'rHits': rHits, 'lMisses': lMisses, 'rMisses': rMisses,
            'lFAs': lFAs, 'rFAs': rFAs, 'lCRs': lCRs, 'rCRs': rCRs, 'lHitRTs': lHitRTs,
            'rHitRTs': rHitRTs, 'lFaRTs': lFaRTs, 'rFaRTs': rFaRTs, 'lHRs': lHRs, 'rHRs': rHRs,
             'lKs': lKs, 'rKs': rKs, 'ldPs': ldPs, 'rdPs': rdPs, 'wHRs': wHRs,
             'wKs': wKs, 'wHitRTs': wHitRTs, 'wFaRTs': wFaRTs, 'wdPs': wdPs}
