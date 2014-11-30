import collections
import random
import math

class QLearningAlgorithm():

    # state: (the nodeId it last was, probability at current XY position) 
    # actions: [0 - index for left lane,1 - index for right lane]
    def __init__(self, actions, discount=0.5, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = collections.Counter()
        self.numIters = 0

    def getPossibleActions(self, state):
        if state[1]:
            return [0]
        return self.actions
        
    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for (f, v) in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.

    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.getPossibleActions(state))
        else:
            possibleQValAndActions = [(self.getQ(state, action), action) for action in
                       self.getPossibleActions(state)]
#             print 'possibleQValAndActions={0}'.format(possibleQValAndActions)
            if len(possibleQValAndActions) == 1:
                return possibleQValAndActions[0][1]
            if possibleQValAndActions[0][0] == possibleQValAndActions[1][0]:
                return random.choice(self.actions)
            return max(possibleQValAndActions)[1]

    # Call this function to get the step size to update the weights.

    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.

    def incorporateFeedback(self, state, action, reward, newState):

        # BEGIN_YOUR_CODE (around 15 lines of code expected)

#         print 's={0} a={1} r={2} sDash={3}'.format(state, action, reward, newState)

        if newState == None:
            return
        residual = reward + self.discount * max([self.getQ(newState,
                aDash) for aDash in self.actions]) - self.getQ(state, action)
        for (f, v) in self.featureExtractor(state, action):
            self.weights[f] = self.weights[f] + self.getStepSize() * residual * v


        # END_YOUR_CODE

# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.

def featureExtractor(state, action):
    featureList = []
    featureList.append((state[0], 1))
#     featureList.append((state[1], 1))
#     featureList.append((state[2], 1))
    if state[2]<0.33:
        featureList.append(('0.33', 1))
    elif state[2]<0.66:
        featureList.append(('0.66', 1))
    else:
        featureList.append(('1.00', 1))
    featureList.append((action, 1))
    return featureList
