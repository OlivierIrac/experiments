'''
Created on 26 juil. 2017

@author: irac1
'''
import random


class FarkleDiceGame:
    dice = [1, 2, 3, 4, 5, 6]
    SEXTUPLET_SCORE = 5000
    QUINTUPLET_SCORE = 2500
    QUADRUPLET_SCORE = 1000
    TRIPLETS_BASE_SCORE = 100
    THREE_ONES_SCORE = 750
    STRAIGHT_SCORE = 2000
    ONE_SCORE = 100
    FIVE_SCORE = 50

    def __init__(self, verbose=False):
        self.__verbose = verbose

    def __verbosePrint(self, *args):
        if (self.__verbose):
            print(*args)

    def evaluateDiceRoll(self, diceRoll):
        score = 0
        diceRoll.sort()
        diceKept = []

        if (len(diceRoll) > 6):
            raise ValueError("Too many dices (max 6)!")

        if (len(diceRoll) >= 4):
            # check for dreaded 4 x 2 => 0
            if (diceRoll.count(2) == 4):
                self.__verbosePrint("Four twos found")
                return (diceKept, 0)

        if (len(diceRoll) == 6):
            # check for sextuplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 6):
                    self.__verbosePrint("Sextuplet found : ", i)
                    diceKept = diceRoll
                    return (diceKept, FarkleDiceGame.SEXTUPLET_SCORE)
            # check for straight 1, 2, 3, 4, 5, 6
            if (diceRoll[0] == 1 and diceRoll[1] == 2 and diceRoll[2] == 3 and diceRoll[3] == 4 and diceRoll[4] == 5 and diceRoll[5] == 6):
                self.__verbosePrint("Straight found")
                diceKept = diceRoll
                return (diceKept, FarkleDiceGame.STRAIGHT_SCORE)

        if (len(diceRoll) >= 5):
            # check for quintuplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 5):
                    self.__verbosePrint("Quintuplet found : ", i)
                    score = FarkleDiceGame.QUINTUPLET_SCORE
                    diceKept = [x for x in diceRoll if x == i]
                    # check for additional one or five (sextuplets of ones and fives already taken care of above)
                    if (i != 1):
                        score += FarkleDiceGame.ONE_SCORE * diceRoll.count(1)
                        diceKept += [1 for x in range(diceRoll.count(1))]
                    if (i != 5):
                        score += FarkleDiceGame.FIVE_SCORE * diceRoll.count(5)
                        diceKept += [5 for x in range(diceRoll.count(5))]
            if (score != 0):
                diceKept.sort()
                return (diceKept, score)

        if (len(diceRoll) >= 4):
            # check for quadruplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 4):
                    self.__verbosePrint("Quadruplet found : ", i)
                    score = FarkleDiceGame.QUADRUPLET_SCORE
                    diceKept = [x for x in diceRoll if x == i]
                    # check for additional ones or fives (sextuplets of ones and fives already taken care of above)
                    if (i != 1):
                        score += FarkleDiceGame.ONE_SCORE * diceRoll.count(1)
                        diceKept += [1 for x in range(diceRoll.count(1))]
                    if (i != 5):
                        score += FarkleDiceGame.FIVE_SCORE * diceRoll.count(5)
                        diceKept += [5 for x in range(diceRoll.count(5))]
            if (score != 0):
                diceKept.sort()
                return (diceKept, score)

        if (len(diceRoll) >= 3):
            # check for three ones
            if (diceRoll.count(1) == 3):
                self.__verbosePrint("Three ones found")
                score = FarkleDiceGame.THREE_ONES_SCORE
                diceKept = [1, 1, 1]
                # check for another triplet
                for i in range(2, 7):
                    if (diceRoll.count(i) == 3):
                        self.__verbosePrint("Second triplet found : ", i)
                        score += FarkleDiceGame.TRIPLETS_BASE_SCORE * i
                        diceKept += [x for x in diceRoll if x == i]
                # check for additional fives, additional ones already taken care of by quadruplets, ... above
                if (score != FarkleDiceGame.THREE_ONES_SCORE + FarkleDiceGame.TRIPLETS_BASE_SCORE * 5):
                    # check for 1 or 2 fives
                    score += FarkleDiceGame.FIVE_SCORE * diceRoll.count(5)
                    diceKept += [5 for x in range(diceRoll.count(5))]
                if (score != 0):
                    diceKept.sort()
                    return (diceKept, score)
            # check for one or two other triplets
            for i in range(2, 7):
                twoTripletsFound = False
                fiveTripletFound = False
                if (diceRoll.count(i) == 3):
                    self.__verbosePrint("Triplet found : ", i)
                    if (i == 5):
                        fiveTripletFound = True
                    score = FarkleDiceGame.TRIPLETS_BASE_SCORE * i
                    diceKept = [x for x in diceRoll if x == i]
                    for j in range(i + 1, 7):
                        if (diceRoll.count(j) == 3):
                            self.__verbosePrint("Second triplet found : ", j)
                            twoTripletsFound = True
                            if (j == 5):
                                fiveTripletFound = True
                            score += FarkleDiceGame.TRIPLETS_BASE_SCORE * j
                            diceKept += [x for x in diceRoll if x == j]
                    if (not twoTripletsFound):
                        # check for additional ones & fives
                        score += FarkleDiceGame.ONE_SCORE * diceRoll.count(1)
                        diceKept += [1 for x in range(diceRoll.count(1))]
                        if (not fiveTripletFound):
                            FarkleDiceGame.FIVE_SCORE * diceRoll.count(5)
                            diceKept += [5 for x in range(diceRoll.count(5))]
                if (score != 0):
                    diceKept.sort()
                    return (diceKept, score)

        # no special combination found, return score for isolated ones and fives
        self.__verbosePrint("No combination found")
        score = FarkleDiceGame.ONE_SCORE * diceRoll.count(1) + FarkleDiceGame.FIVE_SCORE * diceRoll.count(5)
        diceKept += [1 for x in range(diceRoll.count(1))]
        diceKept += [5 for x in range(diceRoll.count(5))]
        return (diceKept, score)


random.seed()
game = FarkleDiceGame(False)

if (False):
    testRolls = [[1, 2, 3, 4, 5, 6, 7],  # too many dices
                 [2, 1, 2, 2, 5, 2],  # four twos
                 [1, 1, 1, 1, 1, 1],  # sextuplets
                 [2, 2, 2, 2, 2, 2],
                 [3, 3, 3, 3, 3, 3],
                 [4, 4, 4, 4, 4, 4],
                 [5, 5, 5, 5, 5, 5],
                 [6, 6, 6, 6, 6, 6],
                 [1, 2, 3, 4, 5, 6],  # straight
                 [1, 1, 1, 1, 1, 2],  # quintuplets
                 [2, 2, 2, 2, 2, 3],
                 [3, 3, 3, 3, 3, 4],
                 [4, 4, 4, 4, 4, 6],
                 [5, 5, 5, 5, 5, 2],
                 [6, 6, 6, 6, 6, 4],
                 [3, 3, 3, 3, 3, 1],  # quintuplets with one or five
                 [2, 2, 2, 2, 2, 5],
                 [1, 1, 1, 1, 2, 2],  # quadruplets
                 [2, 2, 2, 2, 4, 6],
                 [3, 3, 3, 3, 4, 2],
                 [4, 4, 4, 4, 2, 2],
                 [5, 5, 5, 5, 3, 3],
                 [6, 6, 6, 6, 2, 2],
                 [3, 3, 3, 3, 5, 2],  # quadruplets with ones and fives
                 [4, 4, 4, 4, 1, 2],
                 [6, 6, 6, 6, 1, 5],
                 [1, 1, 1, 3, 5, 6],  # three ones
                 [1, 1, 1, 3, 3, 3],  # three ones and other triplet
                 [1, 1, 1, 5, 5, 5],
                 [2, 2, 2, 3, 3, 6],  # other triplets
                 [3, 3, 3, 4, 4, 6],
                 [4, 4, 4, 3, 3, 6],
                 [5, 5, 5, 4, 3, 6],
                 [6, 6, 6, 3, 3, 4],
                 [2, 2, 2, 3, 3, 3],  # two triplets
                 [2, 2, 2, 5, 5, 5]
                 ]
    
    for diceRoll in testRolls:
        print(diceRoll)
        try:
            print(game.evaluateDiceRoll(diceRoll))
        except ValueError as e:
            print (e)
        print()

for _ in range(20):
    diceRoll = []
    nbDices = random.randint(1, 6)
    for dice in range(nbDices):
        diceRoll.append(random.randint(1, 6))
    print (diceRoll)
    print (game.evaluateDiceRoll(diceRoll))
    print()
