from Agent import Agent
import random
import math


class BeliefLearningAgent(Agent):

    def __init__(self, delta, pLambda, informed, payoffMatrixLeft, payOffMatrixRight, sda, p):
        self.weightA = random.random()
        self.weightB = random.random()
        self.delta = delta
        self.informed = informed
        self.pLambda = pLambda
        self.m = [0, 0]
        self.action_weights = [0, 0]
        self.population = ['A', 'B']
        self.actionDict = {"A": 0, "B": 1}
        self.payoffMatrixLeft = payoffMatrixLeft
        self.payoffMatrixRight = payOffMatrixRight
        self.playerNo = 0 if informed == True else 1
        self.p = p
        self.sda = sda  # [stage_dominant_action_Left, stage_dominant_action_Right]

    def reinit_belief(self):
        self.weightA = random.random()
        self.weightB = random.random()

    def update_belief(self, action_by_other_player):
        if (action_by_other_player == 'A'):
            self.weightA = (1 - self.delta) * self.weightA + 1
            self.weightB = (1 - self.delta) * self.weightB
        elif (action_by_other_player == 'B'):
            self.weightA = (1 - self.delta) * self.weightA
            self.weightB = (1 - self.delta) * self.weightB + 1
        self.calculateProbOfActions()

    def calculateProbOfActions(self):
        strength = self.weightA + self.weightB + 1e6
        self.m[0] = self.weightA / strength
        self.m[1] = self.weightB / strength

    def takeAction(self, stage, opp_action, selected):
        action_weights = [1 - self.p, self.p]
        # update belief
        if (opp_action is not None):
            self.update_belief(opp_action)

        if (stage == 1 and self.informed == False):
            # player 2 plays random action:

            actionT = random.choices(self.population, action_weights)
            return actionT[0]

        elif (stage == 2 and self.informed == True):
            # player 1 takes best action possible
            if (selected == 'Left'):
                return self.sda[0]
            else:
                return self.sda[1]

        payOffA = self.calculateExpectedPayOff('A', stage, opp_action, selected)
        payOffB = self.calculateExpectedPayOff('B', stage, opp_action, selected)
        denominator = math.exp(self.pLambda * payOffA) + math.exp(self.pLambda * payOffB)
        action_weights[0] = math.exp(self.pLambda * payOffA) / denominator
        action_weights[1] = math.exp(self.pLambda * payOffB) / denominator
        actionT = random.choices(self.population, action_weights)

        # random.choices returns a list of one item, so we pick the first in the list
        return actionT[0]

    def calculateExpectedPayOff(self, action, stage, opp_action, selected):
        if (stage == 1):
            # Player 1, informed player
            if (selected == 'Left'):
                matrix = self.payoffMatrixLeft
            else:
                matrix = self.payoffMatrixRight
            expectedPayOff = matrix[self.actionDict[action]][0][self.playerNo] * self.m[0] + \
                             matrix[self.actionDict[action]][1][self.playerNo] * self.m[1]
        else:
            # stage 2, uninformed player 2
            matrix_probabilities = self.findMatrixFromSDA(self.m)
            # matrix_probabilities[0] is the prob of left matrix being selected
            expectedPayOff = matrix_probabilities[0] * \
            self.payoffMatrixLeft[self.actionDict[opp_action]][self.actionDict[action]][self.playerNo] 
            + matrix_probabilities[1] * self.payoffMatrixRight[self.actionDict[opp_action]][self.actionDict[action]][
                self.playerNo]
        return expectedPayOff

    def findMatrixFromSDA(self, m):
        # m[0] is the prob tht player 1 played A
        # m[1] is the prob that player 1 played B

        # assume that player 1 always plays optimal action.
        probLeftRight = [0, 0]

        if (self.sda[0] == 'A'):
            probLeftRight[0] = m[0]
        elif (self.sda[0] == 'B'):
            probLeftRight[0] = m[1]

        if (self.sda[1] == 'A'):
            probLeftRight[1] = m[0]
        else:
            probLeftRight[1] = m[1]
        return probLeftRight
