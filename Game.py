import random
import numpy as np


class Game:
    def __init__(self, payOffRight, payOffLeft, p, p1, p2):
        self.payOffRight = payOffRight
        self.payOffLeft = payOffLeft
        self.p = [p, 1 - p]
        self.p1 = p1
        self.p2 = p2
        self.actionDict = {"A": 0, "B": 1}
        self.matrix_choices = ['Left', 'Right']

    def play_round(self):
        selected = random.choices(self.matrix_choices, self.p)
        # stage 1
        # action_state_player huehueheu
        a12 = self.p2.takeAction(stage=1, opp_action=None, selected=None)
        a11 = self.p1.takeAction(stage=1, opp_action=a12, selected=selected)

        a21 = self.p1.takeAction(stage=2, opp_action=None, selected=selected)
        a22 = self.p2.takeAction(stage=2, opp_action=a11, selected=None)

        nparray = np.array([self.getReward(selected, a11, a12), self.getReward(selected, a21, a22)])

        rewards = np.sum(nparray, axis=0)
        s = 0 if selected == 'Left' else 1
        return rewards, a11, a22, s

    def getReward(self, selected, action1, action2):
        if (selected == 'Left'):
            matrix = self.payOffLeft
        else:
            matrix = self.payOffRight

        return matrix[self.actionDict[action1]][self.actionDict[action2]]
