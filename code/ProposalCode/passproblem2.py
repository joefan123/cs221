#!/usr/bin/python

import sys
import collections

import util4

MPHtoFPS = 1.46667      # convert miles per hour to feet per second

class PassingProblem2(util4.MDP):
   
    # The problem is represented by the position of three vehicles on the 2-D grid.
    # State = (CarALane, dist(A,B), dist(A,T))
    # personalityCarB = list of 3 values that represents probability of Car B \
    #                   going Faster, Normal, or Slower
    # Does not allow partial merging
    def __init__(self, speedCarA, speedCarB, speedTruck, distAB, distAT, personalityCarB):
        self.speedCarA = float(speedCarA)
        self.speedCarB = float(speedCarB)
        self.speedTruck = float(speedTruck)
        self.distAB = float(distAB)
        self.distAT = float(distAT)
        self.roadLanes = ['Traffic', 'Opposite']
        self.personalityCarB = personalityCarB
        
    def startState(self):
        return ('Traffic', -1*abs(self.distAB), abs(self.distAT))

    # Return set of actions possible from |state|.
    def actions(self, state):
        return ['Switch', 'Faster', 'Normal', 'Slower']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.        
    def succAndProbReward(self, state, action):

        # Use newDistAB == 0 to signal endgame
        def updateState(newLane, newDistAB, newDistAT):

            # Car A crashes with Car B (gets within 10 feet of it)
            if newLane == 'Traffic' and abs(newDistAB) <= 10:
                newDistAB = None
                
            # Check endgame
            if (newLane == 'Opposite' and newDistAT <= 0) or \
               (newLane == 'Traffic' and newDistAB < 0 and newDistAT <= 0) or \
               (newLane == 'Traffic' and newDistAB >= 200 and newDistAT >= 0): 
                newDistAB = None

            # Out of geographical boundaries (abort)
            if newDistAB < -200. or newDistAB > 300 \
                or newDistAT > 1100 or newDistAT <= 0:
                newDistAB = None
            
            return (newLane, newDistAB, newDistAT)          


        def updateReward(newLane, newDistAB, newDistAT):
            # Car A crashes with truck
            if newLane == 'Opposite' and newDistAT <= 0:
                return -10000

            # Car A crashes with Car B (gets within 10 feet of it)
            if newLane == 'Traffic' and abs(newDistAB) <= 10:
                return -1000
            
            # Car A successfully performs the merge
            # 200 = Distance where Car A merges back, ahead of Car B (typically 200 ft)
            if newLane == 'Traffic' and newDistAB >= 200 and newDistAT >= 0:
                return +100
            
            return -1


        # ---------- Main entry point ----------
        # Initialize and unpack state 
        edges = []
        prevLane, prevDistAB, prevDistAT = state[0], state[1], state[2]
        #print '~'*80
        #print 'prev state: (%s, %s, %s), action: %s' % (prevLane, prevDistAB, prevDistAT, action)

        # Check endgame
        if prevDistAB == None: return edges

        # Process lane change
        if action == 'Switch':
            # Switch Car A's lane
            newLane = list(self.roadLanes)
            newLane.remove(prevLane)
            newLane = newLane[0]
        else:
            newLane = prevLane

        # Calculate vehicle speeds
        if action == 'Faster':      speedMultiplierCarA = 1.1
        elif action == 'Slower':    speedMultiplierCarA = 0.90909090
        else:                       speedMultiplierCarA = 1.0

        # BASELINE SCENARIO !!! CarB action = 'Normal' (always)
        # suppose to use self.personalityCarB
        speedMultiplierCarB = 1.0

        # Calculate relative distances
        newSpeedCarA = self.speedCarA * speedMultiplierCarA
        newSpeedCarB = self.speedCarB * speedMultiplierCarB    
        newDistAB = round(prevDistAB - (newSpeedCarB - newSpeedCarA) * MPHtoFPS)
        newDistAT = round(prevDistAT - (newSpeedCarA - self.speedTruck) * MPHtoFPS)
        #print '  DEBUG newDistAB: %f, newDistAT: %f' % (newDistAB, newDistAT)

        # Prep the edge
        newState = updateState(newLane, newDistAB, newDistAT)
        prob = 1.   # Car A's lane switch is not affected by Car B's personality (???)
        reward = updateReward(newLane, newDistAB, newDistAT)
        #print '  DEBUG reward: %f' % reward
        edges.append((newState, prob, reward))

        # Return edges
        #print 'edges: %s' % edges
        return edges

    def discount(self):
        return 1.    


