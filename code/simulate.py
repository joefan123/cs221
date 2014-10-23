#!/usr/bin/env python
import random, collections, sys

sys.path.append('../Homework/HW4/blackjack')
import passproblem2
import submission, util

def getMDP(scenario):
    if scenario == 0:   # close to AASHTO d2 distance for 60 mph
        return passproblem2.PassingProblem2(speedCarA = 60, speedCarB=60, speedTruck=60, distAB=100, distAT=1000, personalityCarB=[0.3, 0.4, 0.3])
    if scenario == 1:   # about 50% of AASHTO d2 distance for 60 mph
        return passproblem2.PassingProblem2(speedCarA = 60, speedCarB=60, speedTruck=60, distAB=100, distAT=500, personalityCarB=[0.3, 0.4, 0.3])
    if scenario == 2:   # truck is very close! do not pass!
        return passproblem2.PassingProblem2(speedCarA = 60, speedCarB=60, speedTruck=60, distAB=100, distAT=100, personalityCarB=[0.3, 0.4, 0.3])


def runScenario():
    for scenario in range(0,3):
        print
        print '~~~~~~~~~~ BEGIN scenario %d ~~~~~~~~~~' % (scenario)
        mdp = getMDP(scenario)
        vi = submission.ValueIteration()
        vi.solve(mdp)
        f = len([a for a in vi.pi.values() if a == 'Faster']) / float(len(vi.pi.values()))
        print '='*80
        print 'f: %s' % f
        print 'Policy'
        for a in sorted(vi.pi):
            print 'state: %s, pi: %s' % (a, vi.pi.get(a))
        print
    
# ---------- Main entry point ----------
runScenario()

