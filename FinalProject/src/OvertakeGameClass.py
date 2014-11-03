'''
Created on Nov 2, 2014

@author: vinod
'''
from GameStateClass import GameState

class MyClass(object):

    def __init__(self):
        return
        
    def getStartState(self):
        return GameState()
        
    def isEnd(self,gameState):
        return False