import random
import numpy as np
import math

class ReinforcementAgent():
    
    def __init__(self,informed,payoffMatrixLeft, payOffMatrixRight,p, sda, propensityA, propensityB):
        self.informed = informed
        self.m = [0,0]
        self.p = p
        self.strategy = ['A','B']
        self.payoffMatrixLeft = payoffMatrixLeft
        self.payOffMatrixRight = payOffMatrixRight
        self.playerNo = 0 if informed == True else 1
        self.propensityA = propensityA
        self.propensityB = propensityB
        self.sda = sda
    
    #updating the propensity based on Roth - Erev reinforcement model
    def update_propensity(self,payoff, action_by_player):
        if( action_by_player == 'A'):
            self.propensityA = self.propensityA + payoff
            self.propensityB = self.propensityB
        else:
            self.propensityA = self.propensityA
            self.propensityB = self.propensityB + payoff
            
        
    #Action
    def Action(self, stage , selected):
        m = [1-self.p, self.p]
        if(stage == 1 and self.informed == False):
            #player 2 plays random action:
            action =  random.choices(self.strategy, m)
        elif ( stage ==2 and self.informed == True):
            #player 1 takes best action possible
            if(selected == 'Left'):
                return self.sda[0]   #A
            else:
                return self.sda[1]   #B
        strength = self.propensityA + self.propensityB 
        self.m[0] = self.propensityA / strength
        self.m[1] = self.propensityB / strength
        action = random.choices(self.strategy, m)
        return action[0]

              


