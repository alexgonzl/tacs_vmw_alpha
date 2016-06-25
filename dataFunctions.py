
# coding: utf-8

# In[59]:

get_ipython().magic(u'matplotlib inline')


# In[60]:

from __future__ import division
import pandas as pd
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
from collections import OrderedDict
from scipy.stats import norm
Z = norm.ppf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)
np.random.seed(sum(map(ord, "categorical")))


# In[61]:

dataSheets = ['_tacsVWMAlpha.py_2016_May_26_1504_2.csv', '_tacsVWMAlpha.py_2016_May_26_1600.csv', 
'_tacsVWMAlpha.py_2016_May_26_1620.csv', '_tacsVWMAlpha.py_2016_May_26_1639.csv', '_tacsVWMAlpha.py_2016_May_26_1700.csv', 
'_tacsVWMAlpha.py_2016_May_26_1720.csv', '_tacsVWMAlpha.py_2016_May_26_1739.csv']


# In[62]:

conds = OrderedDict([('t2d0', (2, 0)), ('t2d2', (2, 2)), ('t2d4', (2, 4)), ('t4d0', (4, 0)), ('t4d2', (4, 2)), ('t4d4', (4, 4))])


# In[63]:

# counts number of trials corresponding to inputted conditions
def itemCounter(df, responseType, changeType, t, d):
    count = float(len(df[responseType & changeType & t & d]))
    return count


# In[64]:

# calculates K pased on Pashler equation: K = S * ((H - F) / (1 - F))
def kCalculation(s, h, f):
    k = s * ((h - f) / (1 - f))
    return k


# In[65]:

def pashlerK(csv):
    # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    resps = df['Response key'] == 1
    noResps = df['Response key'] == 0
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


# In[66]:

def rtCalc(csv):
    # read in csv file
    df = pd.read_csv(csv)

    # create conditions
    resps = df['Response key'] == 1
    targ2 = df['nTargets'] == 2
    targ4 = df['nTargets'] == 4
    dist0 = df['nDistractors'] == 0
    dist2 = df['nDistractors'] == 2
    dist4 = df['nDistractors'] == 4

    # initialize dictionary
    RTRates = OrderedDict()
    conds = OrderedDict([('t2d0', (targ2, dist0)), ('t2d2', (targ2, dist2)), ('t2d4', (targ2, dist4)), ('t4d0', (targ4, dist0)), ('t4d2', (targ4, dist2)), ('t4d4', (targ4, dist4))])

    # calculate average RT value
    for key in conds:
        rows = df[conds[key][0] & conds[key][1] & resps]
        rts = rows['Response time']
        meanRT = rts.mean()
        RTRates[key] = meanRT
    return RTRates


# In[67]:

def dprime(csv):
     # read in csv file
    df = pd.read_csv(csv)
    
    # create conditions
    resps = df['Response key'] == 1
    noResps = df['Response key'] == 0
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


# In[68]:

Kvals = []
hitRates = []
faRates = []

for sheet in dataSheets:
    Kvals.append(pashlerK(sheet)['Kvals'])
    hitRates.append(pashlerK(sheet)['hitRates'])
    faRates.append(pashlerK(sheet)['fAlarmRates'])


# In[69]:

kMeans = []
kMeanArray = ["K Value Mean"]
hitMeans = []
hitMeanArray = ["Hit Rate Mean"]
faMeans = []
faMeanArray = ["FA Rate Mean"]

for key in conds:
    kMeans.append(Kchart[key].mean())
    hitMeans.append(hitChart[key].mean())
    faMeans.append(faChart[key].mean())


# In[70]:

Kchart = pd.DataFrame(Kvals, index=dataSheets, columns=conds.keys())
Kchart


# In[71]:

hitChart = pd.DataFrame(hitRates, index=dataSheets, columns=conds.keys())
hitChart


# In[72]:

faChart = pd.DataFrame(faRates, index=dataSheets, columns=conds.keys())
faChart


# In[73]:

kMeanChart = pd.DataFrame(kMeans, index=conds.keys(), columns=kMeanArray)
kMeanChart


# In[74]:

hitMeanChart = pd.DataFrame(hitMeans, index=conds.keys(), columns=hitMeanArray)
hitMeanChart


# In[75]:

faMeanChart = pd.DataFrame(faMeans, index=conds.keys(), columns=faMeanArray)
faMeanChart


# In[76]:

RTvals = []

for sheet in dataSheets:
    RTvals.append(rtCalc(sheet))

RTchart = pd.DataFrame(RTvals, index=dataSheets, columns=conds.keys())
RTchart


# In[77]:

rtMeanArray = ["RT Mean"]

rtMeans = []

for key in conds:
    rtMeans.append(RTchart[key].mean())
    
rtMeanChart = pd.DataFrame(rtMeans, index=conds.keys(), columns=rtMeanArray)
rtMeanChart


# In[78]:

dPrimes = []

for sheet in dataSheets:
    dPrimes.append(dprime(sheet))

dpChart = pd.DataFrame(dPrimes, index=dataSheets, columns=conds.keys())
dpChart


# In[79]:

dpMeanArray = ["d' Mean"]

dpMeans = []

for key in conds:
    dpMeans.append(dpChart[key].mean())
    
dpMeanChart = pd.DataFrame(dpMeans, index=conds.keys(), columns=dpMeanArray)
dpMeanChart


# In[80]:

sns.barplot(data=Kchart)


# In[81]:

sns.stripplot(data=Kchart)


# In[ ]:



