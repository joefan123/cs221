import collections, util4, math, random

############################################################

############################################################
# Problem 2a

class ValueIteration(util4.MDPAlgorithm):

    # Implement value iteration.  First, compute V_opt using the methods 
    # discussed in class.  Once you have computed V_opt, compute the optimal 
    # policy pi.  Note that ValueIteration is an instance of util.MDPAlgrotithm, 
    # which means you will need to set pi and V (see util.py).
    def solve(self, mdp, epsilon=0.001):
        mdp.computeStates()
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        #print 'len(mdp.states): %s' % (len(mdp.states))

        # Initialize
        t = 0; V_opt = {}; pi = {}; converge = False
        for state in mdp.states:
            V_opt[(t, state)] = 0.
        
        # Begin value iteration
        while t < 500 and converge == False:
            # Initialize iteration
            t += 1; Q_opt = {}; convergeCount = 0
            #print '-'*20, 'iteration: ', t
            
            # Calculate V_opt
            for state in mdp.states:
                #print 'state: %s' % state
                #print 'state: (%s, %s, %s)' % (state[0], state[1], state[2])
                V_opt[(t, state)] = None  ### fix 1
                for action in mdp.actions(state):
                    #print '    action: %s' % action
                    Q_opt[(state, action)] = 0.
                    #V_opt[(t, state)] = None   ### bug 1
                    for newState, prob, reward in mdp.succAndProbReward(state, action):
                        #print '        newState: %s, prob: %s, reward: %s, mdp.discount: %s, V_opt[(t-1, newState)]: %s, t: %d' % (newState, prob, reward, mdp.discount(), V_opt[(t-1, newState)], t)
                        Q_opt[(state, action)] += prob * (reward + mdp.discount() * V_opt[(t-1, newState)])
                    #print '        Q_opt[(state, action)]: %f' % (Q_opt[(state, action)])
                    if V_opt[(t, state)] == None or Q_opt[(state, action)] >= V_opt[(t, state)]:
                        V_opt[(t, state)] = Q_opt[(state, action)]
                        pi[state] = action
                #print '==> V_opt[(t, state)]: %f, V_opt[(t, state)]: %f , pi[state]: %s, t: %d' % (V_opt[(t, state)], V_opt[(t-1, state)], pi[state], t)
                
                # Check convergence for state
                if abs(V_opt[(t, state)] - V_opt[(t-1, state)]) < epsilon:
                    convergeCount += 1
                    
            # Check convergence for all states
            #print 'convergeCount: %d' % convergeCount
            if convergeCount == len(mdp.states):
                converge = True

        # Return answers
        self.V = {}
        for state in sorted(mdp.states):
            #print 'V_opt[(%s, %s)]: %s' % (t, state, V_opt[(t, state)])
            self.V[state] = V_opt[(t, state)]
        self.pi = dict(pi)
        # END_YOUR_CODE
        

