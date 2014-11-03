'''
Created on Nov 2, 2014

@author: vinod
'''

class Vehicle(object):

    def __init__(self, name, speed=1, topSpeed=3, accelerationStep=1, nature='constant',position=(0,0)):
        self.name = name  # A/B/T
        self.speed = speed  # how much a vehicle moves per tick
        self.topSpeed = topSpeed  # upper bound of speed
        self.accelerationStep = accelerationStep  # amount speed changes when we accelerate
        self.position=position
        if self.name == 'T':
            self.nature = 'constant'
        else:
            self.nature = nature  # constant, random or adversary
        
    # returns all legal actions for a given GameStateClass
    def getLegalActions(self, gameState):
        return None
    
    # change 'gameState' based on 'action'
    def applyAction(self, action):
        return None