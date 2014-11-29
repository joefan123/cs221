'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
from engine.model.car.junior import Junior
from engine.model.car.car import Car

import util
import random

# Class: AutoDriver
# ---------------------
# An initially naive autonomous driver that drives around a map, avoiding cars
# based on beliefs. Feel free to extend this class. It is *not* required!
class AutoDriver(Junior):

    MIN_PROB = 0.02
    
    # Funciton: Init
    # ---------------------
    # Create an autonomous driver. Give it a number of heartBeats to wait before
    # it starts to drive
    def __init__(self, QLearner):
        self.nodeId = None
        self.nextId = None
        self.nextNode = None
        self.burnInIterations = 10
        
        self.QLearner = QLearner
        self.prevState = None
        self.prevActionIndex = None
    
    # Funciton: Get Autonomous Actions
    # ---------------------
    # Given the current belief about where other cars are and a graph of how
    # one can driver around the world, chose a next action.

    def getAutonomousActions(self, beliefOfOtherCars, agentGraph):
        
        # Don't start until after your burn in iterations have expired
        if self.burnInIterations > 0:
            return[]
        
        # actions = self.Baseline(beliefOfOtherCars, agentGraph)
        actions = self.QLearn(beliefOfOtherCars, agentGraph)
        return actions
    
    def incorporateRewardInQLearn(self, reward, beliefOfOtherCars):
        if self.burnInIterations > 0:
            self.burnInIterations -= 1
            return
        
        newState = self.formState(beliefOfOtherCars)
        self.QLearner.incorporateFeedback(self.prevState, self.prevActionIndex, reward, newState)
        
#         print 'weights={0}'.format(self.QLearner.weights)
            
    def QLearn(self, beliefOfOtherCars, agentGraph):
        
        if self.nodeId == None:
            self.nodeId = agentGraph.getNearestNode(self.pos)
        if self.nextId != None and agentGraph.atNode(self.nextId, self.pos):
            self.nodeId = self.nextId
            
        state = self.formState(beliefOfOtherCars)
        self.prevState = state
        nodeIndex = self.QLearner.getAction(state)
#         print 'nodeIndex={0}'.format(nodeIndex)
        self.prevActionIndex = nodeIndex
        nextIds = agentGraph.getNextNodeIds(self.nodeId)
#         print 'nodeId:{0} nextIds:{1}'.format(self.nodeId, nextIds)
        self.nextId = nextIds[nodeIndex]
#         print 'nextId={0}'.format(self.nextId)
        
        actions = self.GetActionsForNodeId(beliefOfOtherCars, agentGraph, self.nextId)
        return actions
         
    def formState(self, beliefOfOtherCars):
        return (self.nodeId, self.getProbAtPos(beliefOfOtherCars, self.pos))

    def Baseline(self, beliefOfOtherCars, agentGraph):
        if self.nodeId == None:
            self.nodeId = agentGraph.getNearestNode(self.pos)
        if self.nextId == None:
            self.choseNextId_Baseline(agentGraph, beliefOfOtherCars)
        if agentGraph.atNode(self.nextId, self.pos):
            self.nodeId = self.nextId
            self.choseNextId_Baseline(agentGraph, beliefOfOtherCars)
        actions = self.GetActionsForNodeId(beliefOfOtherCars, agentGraph, self.nextId)
        return actions
    
    def GetActionsForNodeId(self, beliefOfOtherCars, agentGraph, nodeId):
        goalPos = agentGraph.getNode(nodeId).getPos()
        vectorToGoal = goalPos - self.pos
        wheelAngle = -vectorToGoal.get_angle_between(self.dir)
        driveForward = not self.isCloseToOtherCar(beliefOfOtherCars)
        actions = {Car.TURN_WHEEL:wheelAngle}
        if driveForward:
            actions[Car.DRIVE_FORWARD] = 1.0
        return actions
    
    # Funciton: Is Close to Other Car
    # ---------------------
    # Given the current belief about where other cars are decides if
    # there is a car in the spot where we are about to drive. 
    def isCloseToOtherCar(self, beliefOfOtherCars):
        newBounds = []
        # The multiplier was 1.5
        offset = self.dir.normalized() * 1 * Car.LENGTH
        newPos = self.pos + offset
        row = util.yToRow(newPos.y)
        col = util.xToCol(newPos.x)
        p = beliefOfOtherCars.getProb(row, col)
        # print 'row:{0} col:{1} prob:{2}'.format(row,col,p);
        return p > AutoDriver.MIN_PROB
    
    def isCarAtPos(self, beliefOfOtherCars, pos):
        p = self.getProbAtPos(beliefOfOtherCars, pos)
        # print 'row:{0} col:{1} prob:{2}'.format(row,col,p);
        return p > AutoDriver.MIN_PROB
    
    def getProbAtPos(self, beliefOfOtherCars, pos):
        row = util.yToRow(pos.y)
        col = util.xToCol(pos.x)
        p = beliefOfOtherCars.getProb(row, col)
        return p
    
    # Funciton: Chose Next Id
    # ---------------------
    # You have arrived at self.nodeId. Chose a next node to drive
    # towards.
    def choseNextId_Baseline(self, agentGraph, beliefOfOtherCars):
        nextIds = agentGraph.getNextNodeIds(self.nodeId)
        print 'nodeId:{0} nextIds:{1}'.format(self.nodeId, nextIds)
        if nextIds == []: 
            self.nextId = None
        else:
            self.nextId = nextIds[0]
            if self.isCarAtNode(beliefOfOtherCars, agentGraph.getNode(self.nextId).getPos()):
                self.nextId = nextIds[1]
        print 'nextId:{0}'.format(self.nextId)
