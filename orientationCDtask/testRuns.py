from collections import OrderedDict

lstimTestRuns = [(2,1),(3,2),(4,3),(5,2),(6,3),(7,1)]
rstimTestRuns = [(2,3),(3,1),(4,1),(5,3),(6,2),(7,2)]
shamTestRuns = [(2,2),(3,3),(4,2),(5,1),(6,1),(7,3)]
HFconds = OrderedDict([('t1d0', (1, 0)), ('t1d1', (1, 1)), ('t1d2', (1, 2)), ('t2d0', (2, 0)), ('t2d1', (2, 1)), ('t2d2', (2, 2))])
WFconds = OrderedDict([('t2d0', (2, 0)), ('t2d2', (2, 2)), ('t2d4', (2, 4)), ('t4d0', (4, 0)), ('t4d2', (4, 2)), ('t4d4', (4, 4))])

#pilotTestRuns = [(1,1),(1,2),(1,3)]
pilotTestRuns = [(2,1),(2,2)]
