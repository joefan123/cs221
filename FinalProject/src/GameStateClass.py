'''
Created on Nov 2, 2014

@author: vinod
'''
from VehicleClass import Vehicle

class GameState(object):

    def __init__(self, height, width, vehicles=None):
        self.height = height
        self.width = width
        if vehicles!=None:
            self.vehicles = vehicles # dict of vehicle name as key & VehicleClass object as value
        else:
            self.vehicles=dict()
            self.vehicles['A']=Vehicle(name='A')
            self.vehicles['B']=Vehicle(name='B')
            self.vehicles['T']=Vehicle(name='C')
        