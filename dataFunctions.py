# pandas import
import pandas as pd
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier

# calculates rates based on intersecting conditions
def rateCalculation(df, r, t, d, change):
    rate = float(len(df[r & change & t & d])) / len(df[change & t & d])
    return rate

# calculates K pased on Pashler equation: K = S * ((H - F) / (1 - F))
def kCalculation(s, h, f):
    k = s * ((h - f) / (1 - f))
    return k

def pashlerK(csv):
    # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    resps = df['Response'] == 1
    changes = df['ChangeTrial'] == 1
    noChanges = df['ChangeTrial'] == 0
    targ2 = df['nTargets'] == 2
    targ4 = df['nTargets'] == 4
    dist0 = df['nDistractors'] == 0
    dist2 = df['nDistractors'] == 2
    dist4 = df['nDistractors'] == 4

    # initialize dictionaries
    hitRates = {}
    fAlarmRates = {}
    Kvals = {}

    conds = {'t2d0': (targ2, dist0), 't2d2': (targ2, dist2), 't2d4': (targ2, dist4), 't4d0': (targ4, dist0), 't4d2': (targ4, dist2), 't4d4': (targ4, dist4)}
    
    # store rate values
    for key in conds:
        hitRates[key] = rateCalculation(df, resps, conds[key][0], conds[key][1], changes)
        fAlarmRates[key] = rateCalculation(df, resps, conds[key][0], conds[key][1], noChanges)
        s = 0
        if key == 't2d0' or key == 't2d2' or key == 't2d4':
            s = 2
        else:
            s = 4
        Kvals[key] = kCalculation(s, hitRates[key], fAlarmRates[key])
    return Kvals

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
    RTRates = {}
    conds = {'t2d0': (targ2, dist0), 't2d2': (targ2, dist2), 't2d4': (targ2, dist4), 't4d0': (targ4, dist0), 't4d2': (targ4, dist2), 't4d4': (targ4, dist4)}

    # calculate average RT value
    for key in conds:
        rows = df[conds[key][0] & conds[key][1] & resps]
        rts = rows['RT']
        meanRT = rts.mean()
        RTRates[key] = meanRT
    return RTRates
