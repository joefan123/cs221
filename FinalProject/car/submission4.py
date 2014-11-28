import collections, util, math, random

############################################################

############################################################
# Problem 2a

class ValueIteration(util.MDPAlgorithm):

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
        

############################################################
# Problem 2b

# If you decide 2b is true, prove it in writeup.pdf and put "return None" for
# the code blocks below.  If you decide that 2b is false, construct a
# counterexample by filling out this class and returning an alpha value in
# counterexampleAlpha().
class CounterexampleMDP(util.MDP):
    def __init__(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        self.n = 2
        # END_YOUR_CODE

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return 0
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return [-1, +1]
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        edges = list()
        origProb = {action:(action<0)*1. for action in self.actions(state)}
        for action in self.actions(state):
            newState = min(max(state + action, -self.n), +self.n)
            prob = (origProb.get(action) + counterexampleAlpha()) / sum(origProb.get(action) + counterexampleAlpha() for action in origProb)
            if action < 0: reward = 1.
            else: reward = 10.
            edges.append((newState, prob, reward))
        return edges
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return 0.9
        # END_YOUR_CODE

def counterexampleAlpha():
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return 0.1
    # END_YOUR_CODE

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.  The second element is the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.  The final element
    # is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to (0,).
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 55 lines of code expected)

        def updateState(prevScore, peekIdx, prevDeck, newCard):
            # Initialize deck
            newDeck = list(prevDeck)
            
            if newCard is not None:     # action = 'Take'
                # Update deck
                if newDeck[self.cardValues.index(newCard)] > 0:
                    newDeck[self.cardValues.index(newCard)] -= 1
                else:
                    newDeck = None
            
                # Check peek
                if peekIdx is not None:
                    newPeekCost = self.peekCost
                    newPeekIdx = None
                else:
                    newPeekCost = 0
                    newPeekIdx = peekIdx
            else:   # action = 'Peek'
                # Check peek
                newPeekCost = self.peekCost
                newPeekIdx = peekIdx
                newCard = 0
            
            # Update score and deck
            newScore = prevScore + newCard
            if newDeck is not None:
                if newScore > self.threshold or sum(i for i in newDeck) == 0:
                    newDeck = None
                else:
                    newDeck = tuple(newDeck)
            
            # Return updated state
            return (newScore, newPeekIdx, newDeck)

        def updateReward(action, newScore, newDeck):
            if action == 'Take':
                if newDeck is not None:
                    return 0
                else:
                    if newScore > self.threshold:
                        return 0
                    else:
                        return newScore
            elif action == 'Peek':
                return -1 * self.peekCost

        # ---------- Main entry point ----------
        # Initialize and unpack state 
        edges = []
        newScore = 0; newCard = 0; newPeekCost = 0; newPeekIdx = None
        prevScore, prevPeekIdx, prevDeck = state[0], state[1], state[2]
        #print '~'*80
        #print 'prev state: (%s, %s, %s)' % (prevScore, prevPeekIdx, prevDeck)
        
        # Check endgame
        if prevDeck is None: return edges

        # Process the action
        if action == 'Take':
            if prevPeekIdx is None:
                # Take random card
                for newCard in self.cardValues:
                    newCardIdx = self.cardValues.index(newCard)
                    prob = float(prevDeck[newCardIdx]) / sum(i for i in prevDeck)
                    if prob == 0: continue
                    newState = updateState(prevScore, prevPeekIdx, prevDeck, newCard)
                    reward = updateReward(action, newState[0], newState[2])
                    #print '    action: Take, new state: (%s, %s, %s), prob: %s, reward: %s' % (newState[0], newState[1], newState[2], prob, reward)
                    edges.append((newState, prob, reward))
            else:
                # Take peeked card
                newCard = self.cardValues[prevPeekIdx]
                prob = 1.
                newState = updateState(prevScore, None, prevDeck, newCard)
                reward = updateReward(action, newState[0], newState[2])
                #print '    action: Take, new state: (%s, %s, %s), prob: %s, reward: %s' % (newState[0], newState[1], newState[2], prob, reward)
                edges.append((newState, prob, reward))
        elif action == 'Peek':
            if prevPeekIdx is None:
                # Peek card and update deck
                for peekCard in self.cardValues:
                    if prevDeck[self.cardValues.index(peekCard)] > 0:
                        peekCardIdx = self.cardValues.index(peekCard)
                        prob = float(prevDeck[peekCardIdx]) / sum(i for i in prevDeck)
                        newState = updateState(prevScore, peekCardIdx, prevDeck, None)
                        reward = updateReward(action, newState[0], newState[2])
                        #print '    action: Peek, new state: (%s, %s, %s), prob: %s, reward: %s' % (newState[0], newState[1], newState[2], prob, reward)
                        edges.append((newState, prob, reward))
            else:
                # If the player peeks twice in a row, return []
                pass
        elif action == 'Quit':
            newState = (prevScore, None, None)
            prob = 1.
            reward = prevScore
            edges.append((newState, prob, reward))

        # Return edges
        return edges
               
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return BlackjackMDP(cardValues=[1,4,5,20], multiplicity=2, threshold=20, peekCost=1)  # f = 0.14
    
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = collections.Counter()
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        # Check endgame
        if newState is None: return
            
        # Calculate residual
        maxQ = None
        for newAction in self.actions(newState):
            tempQ = self.getQ(newState, newAction)
            if tempQ > maxQ or maxQ is None:
                maxQ = tempQ
        residual = (reward + self.discount * maxQ) - self.getQ(state, action)
        
        # Update weights
        phi = self.featureExtractor(state, action)
        stepSize = self.getStepSize()
        for i in range(len(phi)):
            featureKey, featureValue = phi[i][0], phi[i][1]
            self.weights[featureKey] = self.weights.get(featureKey, 0) + stepSize * residual * featureValue

        # END_YOUR_CODE

# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning

# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).  Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE (around 10 lines of code expected)
    # Initialize
    featureList = list()
    
    # indicator on the total and the action (1 feature).
    featureList.append( (("TOTAL", total, action), 1) )
    
    if counts is not None:
        # indicator on the presence/absence of each card and the action (1 feature).  Only add this feature if the deck != None
        presence = tuple([(i > 0)*1 for i in counts])
        featureList.append( (("PRESENCE", presence, action), 1) )

        # indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
        for cardIdx in range(len(counts)):
            featureList.append( (("CARDCOUNT", cardIdx, counts[cardIdx], action), 1) )
    
    return featureList
    # END_YOUR_CODE

############################################################
# Problem 4d: changing mdp

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)
