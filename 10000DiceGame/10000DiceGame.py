'''
Created on 26 juil. 2017

@author: irac1
'''
import random
import logging as log

# TODO: verbose with types
verboseLevel = 2


def verbose(level, *args):
    if(level > verboseLevel):
        print(*args)


class GameStatistics:
    def __init__(self):
        self.totalScore = 0
        self.nonZeroTotalScore = 0
        self.combination = 0
        self.nonZeroCombination = 0
        self.maxScore = 0

    def print(self):
        msg = "max score = " + str(self.maxScore) + "\n"
        msg += "average score per roll = " + str(self.totalScore / self.combination) + "\n"
        msg += "average score per non nul roll = " + repr(self.nonZeroTotalScore / self.nonZeroCombination) + "\n"
        msg += str(self.combination) + " combinations\n"
        msg += str(self.combination - self.nonZeroCombination) + " nul combinations = " + repr(100 * (self.combination - self.nonZeroCombination) / self.combination) + "% \n"
        return msg


class Player:
    def __init__(self, game, name=""):
        self.name = name
        self.score = 0
        self.game = game
        self.turnScore = 0
        self.hasStarted = False

    def startTurn(self):
        self.turnScore = 0
        self.turnDicesKept = []
        # TODO: separate user interaction
        print("\n----- Next player -----")

    def decideNextMove(self, diceRoll):
        raise NotImplementedError()  # pure virtual

    def addTurnScore(self, score, dicesKept):
        self.turnScore += score
        if(len(dicesKept) > 0):
            self.turnDicesKept += dicesKept
        else:
            self.turnDicesKept = []

    def status(self, diceRoll=[]):
        # TODO: separate user interaction
        print (self.name, "Roll:", diceRoll, "Kept:", self.turnDicesKept, "Turn score:", self.turnScore, "Total score:", self.score)

    def endTurn(self, turnScore, diceRoll):
        if(turnScore):
            if(self.hasStarted or self.turnScore >= FarkleDiceGame.START_SCORE):
                self.score += self.turnScore
                self.hasStarted = True
        else:
            # TODO: separate user interaction
            print("Too bad !!!")
        self.status(diceRoll)


class ComputerPlayer(Player):
    def __init__(self, game, name="", riskFactor=1.0):
        super().__init__(game, name)
        self.riskFactor = riskFactor

    def decideNextMove(self, diceRoll):
        (diceKept, score) = self.game.evaluateDices(diceRoll)
        self.status(diceRoll)
        if(not self.hasStarted):
            # not started, keep playing until reach score required for start
            if(score + self.turnScore < FarkleDiceGame.START_SCORE):
                return (True, diceKept)
            else:
                return (False, diceKept)
        else:
            # started
            # evaluate benefit of continuing
            scoreIfDoNotContinue = score + self.turnScore
            remainingDices = len(diceRoll) - len(diceKept)
            # TODO: refactor statistics
            potentialScoreIfContinue = self.game.gameStats[remainingDices].nonZeroCombination / self.game.gameStats[remainingDices].combination * (score + self.turnScore + self.game.gameStats[remainingDices].nonZeroTotalScore / self.game.gameStats[remainingDices].nonZeroCombination)
            # TODO: implement optimization for discarding 1 or 5
            print(scoreIfDoNotContinue, potentialScoreIfContinue, self.riskFactor * potentialScoreIfContinue)
            if(self.riskFactor * potentialScoreIfContinue > scoreIfDoNotContinue and self.score + potentialScoreIfContinue < FarkleDiceGame.WIN_SCORE):
                # continue if potential score by throwing dices again > current score and does not exceed win score
                return (True, diceKept)
            else:
                return (False, diceKept)


class HumanPlayer(Player):
    def __init__(self, game, name=""):
        super().__init__(game, name)

    def decideNextMove(self, diceRoll):
        self.status(diceRoll)
        diceKept = []
        diceAvail = diceRoll
        (diceAllowed, _) = self.game.evaluateDices(diceRoll)
        done = False
        keepPlaying = True
        while(not done):
            # TODO: separate user interaction
            dice = input("keep dice (empty to end)? ")
            if (dice in ['1', '2', '3', '4', '5', '6']):
                dice = int(dice)
                # TODO: separate check of valid user inputs / selections
                if (dice in diceAvail and dice in diceAllowed):
                    diceKept.append(dice)
                    diceAvail.remove(dice)
                else:
                    # TODO: separate user interaction
                    print("Not allowed")
            elif (dice != ''):
                done = True
                keepPlaying = False
            else:
                done = True
        # FIXME: check that hand is still valid (possible refactor in game class) ex. from 1, 2, 2, 2 currently possible to take 1, 2
        return (keepPlaying, diceKept)


class FarkleDiceGame:
    dice = [1, 2, 3, 4, 5, 6]
    # TODO: extract rules in separate class
    SEXTUPLET_SCORE = 5000
    QUINTUPLET_SCORE = 2500
    QUADRUPLET_SCORE = 1000
    TRIPLETS_BASE_SCORE = 100
    THREE_ONES_SCORE = 750
    STRAIGHT_SCORE = 2000
    ONE_SCORE = 100
    FIVE_SCORE = 50
    WIN_SCORE = 10000
    START_SCORE = 750

    def __init__(self):
        self.players = []
        self.gameStats = []
        self.turn = 0
        random.seed()
        # TODO: save / restore stats to file
        for i in FarkleDiceGame.dice:
            self.gameStats.append(self.__computeStatistics(i))
            msg = str(i) + " dices\n" + self.gameStats[i - 1].print()
            verbose(2, msg)

    def __keepOnes(self, diceRoll, diceKept, score):
        score += FarkleDiceGame.ONE_SCORE * diceRoll.count(1)
        diceKept += [1 for _ in range(diceRoll.count(1))]
        return (diceKept, score)

    def __keepFives(self, diceRoll, diceKept, score):
        score += FarkleDiceGame.FIVE_SCORE * diceRoll.count(5)
        diceKept += [5 for _ in range(diceRoll.count(5))]
        return (diceKept, score)

    def __computeStatistics(self, nbDices, diceRoll=[], stats=0, init=True):
        # TODO: refactor stats
        if(init):
            stats = GameStatistics()
        if(nbDices == 1):
            for dice in FarkleDiceGame.dice:
                stats.combination += 1
                (_, score) = self.evaluateDices(diceRoll + [dice])
                stats.totalScore += score
                if (score != 0):
                    stats.nonZeroCombination += 1
                    stats.nonZeroTotalScore += score
                if(score > stats.maxScore):
                    stats.maxScore = score
        else:
            for dice in FarkleDiceGame.dice:
                stats = self.__computeStatistics(nbDices - 1, diceRoll + [dice], stats, False)
        return stats

    def addPlayer(self, name="", kind="computer", riskFactor=1.0):
        if(kind == "computer"):
            self.players.append(ComputerPlayer(self, name, riskFactor))
        if(kind == "human"):
            self.players.append(HumanPlayer(self, name))

    def rollDices(self, nbDices):
        diceRoll = []
        for _ in range(nbDices):
            diceRoll.append(random.choice(FarkleDiceGame.dice))
        return diceRoll

    def play(self):
        gameOver = False
        currentPlayer = 0
        print(len(self.players), "players:")
        for player in self.players:
            print (player.name)
        turn = 1
        while(not gameOver):
            self.players[currentPlayer].startTurn()
            turnOver = False
            # TODO: implement turn follow up (resume from dices from previous player)
            nbDicesToThrow = 6
            while (not turnOver):
                diceRoll = self.rollDices(nbDicesToThrow)
                (_, maxScore) = self.evaluateDices(diceRoll)
                if(maxScore == 0):
                    self.players[currentPlayer].endTurn(False, diceRoll)
                    turnOver = True
                else:
                    (keepPlaying, diceKept) = self.players[currentPlayer].decideNextMove(diceRoll)                        
                    (_, turnScore) = self.evaluateDices(diceKept)
                    nbDicesToThrow -= len(diceKept)
                    if(nbDicesToThrow <= 0):
                        keepPlaying = True  # must continue if no more dice
                        nbDicesToThrow = 6
                        diceKept = []
                    self.players[currentPlayer].addTurnScore(turnScore, diceKept)
                    if(turnScore == 0 or self.players[currentPlayer].score + self.players[currentPlayer].turnScore > FarkleDiceGame.WIN_SCORE):
                        self.players[currentPlayer].endTurn(False, diceRoll)
                        turnOver = True
                    elif (not keepPlaying):
                        self.players[currentPlayer].endTurn(True, diceRoll)
                        turnOver = True
            if (self.players[currentPlayer].score == FarkleDiceGame.WIN_SCORE):
                # TODO: separate user interaction
                print(self.players[currentPlayer].name, "wins !!!")
                print(turn, "turns")
                for player in self.players:
                    print(player.name, player.score)
                gameOver = True

            currentPlayer += 1
            if (currentPlayer == len(self.players)):
                currentPlayer = 0
                turn += 1
        return currentPlayer

    def evaluateDices(self, diceRoll):
        score = 0
        # TODO: avoid sort (used only for straight detection)
        diceRoll.sort()
        diceKept = []

        if (len(diceRoll) > 6):
            raise ValueError("Too many dices (max 6)!")

        if (len(diceRoll) >= 4):
            # check for dreaded 4 x 2 => 0
            if (diceRoll.count(2) == 4):
                verbose(1, "Four twos found")
                return (diceKept, 0)

        if (len(diceRoll) == 6):
            # check for sextuplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 6):
                    verbose(1, "Sextuplet found : " + str(i))
                    diceKept = diceRoll
                    return (diceKept, FarkleDiceGame.SEXTUPLET_SCORE)
            # check for straight 1, 2, 3, 4, 5, 6
            if (diceRoll[0] == 1 and diceRoll[1] == 2 and diceRoll[2] == 3 and diceRoll[3] == 4 and diceRoll[4] == 5 and diceRoll[5] == 6):
                verbose(1, "Straight found")
                diceKept = diceRoll
                return (diceKept, FarkleDiceGame.STRAIGHT_SCORE)

        if (len(diceRoll) >= 5):
            # check for quintuplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 5):
                    verbose(1, "Quintuplet found : " + str(i))
                    score = FarkleDiceGame.QUINTUPLET_SCORE
                    diceKept = [x for x in diceRoll if x == i]
                    # check for additional one or five (sextuplets of ones and fives already taken care of above)
                    if (i != 1):
                        (diceKept, score) = self.__keepOnes(diceRoll, diceKept, score)
                    if (i != 5):
                        (diceKept, score) = self.__keepFives(diceRoll, diceKept, score)

            if (score != 0):
                diceKept.sort()
                return (diceKept, score)

        if (len(diceRoll) >= 4):
            # check for quadruplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 4):
                    verbose(1, "Quadruplet found : " + str(i))
                    score = FarkleDiceGame.QUADRUPLET_SCORE
                    diceKept = [x for x in diceRoll if x == i]
                    # check for additional ones or fives (sextuplets of ones and fives already taken care of above)
                    if (i != 1):
                        (diceKept, score) = self.__keepOnes(diceRoll, diceKept, score)
                    if (i != 5):
                        (diceKept, score) = self.__keepFives(diceRoll, diceKept, score)
            if (score != 0):
                diceKept.sort()
                return (diceKept, score)

        if (len(diceRoll) >= 3):
            # check for three ones
            if (diceRoll.count(1) == 3):
                verbose(1, "Three ones found")
                score = FarkleDiceGame.THREE_ONES_SCORE
                diceKept = [1, 1, 1]
                # check for another triplet
                for i in range(2, 7):
                    if (diceRoll.count(i) == 3):
                        verbose(1, "Second triplet found : " + str(i))
                        score += FarkleDiceGame.TRIPLETS_BASE_SCORE * i
                        diceKept += [x for x in diceRoll if x == i]
                # check for additional fives, additional ones already taken care of by quadruplets, ... above
                if (score != FarkleDiceGame.THREE_ONES_SCORE + FarkleDiceGame.TRIPLETS_BASE_SCORE * 5):
                    # check for 1 or 2 fives
                    (diceKept, score) = self.__keepFives(diceRoll, diceKept, score)
                if (score != 0):
                    diceKept.sort()
                    return (diceKept, score)
            # check for one or two other triplets
            for i in range(2, 7):
                twoTripletsFound = False
                fiveTripletFound = False
                if (diceRoll.count(i) == 3):
                    verbose(1, "Triplet found : " + str(i))
                    if (i == 5):
                        fiveTripletFound = True
                    score = FarkleDiceGame.TRIPLETS_BASE_SCORE * i
                    diceKept = [x for x in diceRoll if x == i]
                    for j in range(i + 1, 7):
                        if (diceRoll.count(j) == 3):
                            verbose(1, "Second triplet found : " + str(j))
                            twoTripletsFound = True
                            if (j == 5):
                                fiveTripletFound = True
                            score += FarkleDiceGame.TRIPLETS_BASE_SCORE * j
                            diceKept += [x for x in diceRoll if x == j]
                    if (not twoTripletsFound):
                        # check for additional ones & fives
                        (diceKept, score) = self.__keepOnes(diceRoll, diceKept, score)
                        if (not fiveTripletFound):
                            (diceKept, score) = self.__keepFives(diceRoll, diceKept, score)
                if (score != 0):
                    diceKept.sort()
                    return (diceKept, score)

        # no special combination found, return score for isolated ones and fives
        verbose(1, "No combination found")
        (diceKept, score) = self.__keepOnes(diceRoll, diceKept, score)
        (diceKept, score) = self.__keepFives(diceRoll, diceKept, score)
        return (diceKept, score)


def testCases():
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
                 [2, 2, 2, 5, 5, 5],
                 [2, 2, 2, 1, 3, 6],  # other triplets with ones and fives
                 [3, 3, 3, 5, 4, 6],
                 [4, 4, 4, 1, 5, 6]
                 ]

    game = FarkleDiceGame()
    for diceRoll in testRolls:
        print(diceRoll)
        try:
            print(game.evaluateDices(diceRoll))
        except ValueError as e:
            print (e)
        print()


def randomCheck():
    game = FarkleDiceGame()
    for _ in range(20):
        nbDices = random.choice(FarkleDiceGame.dice)
        diceRoll = game.rollDices(nbDices)
        print (diceRoll)
        print (game.evaluateDices(diceRoll))
        print()


def playComputersGame():
    winners = [0 for _ in range(5)]
    for i in range(100):
        game = FarkleDiceGame()
#    game.addPlayer("Louis", "human")
#    game.addPlayer("Olivier", "human")
        game.addPlayer("Ordi 0.5", "computer", 0.5)
        game.addPlayer("Ordi 0.8", "computer", 0.8)
        game.addPlayer("Ordi 1.0")
        game.addPlayer("Ordi 1.5", "computer", 1.5)
        game.addPlayer("Ordi 2.0", "computer", 2.0)
        winner = game.play()
        winners[winner - 1] += 1
        print("Game #", i)
    print(winners)


def playHumanVsComputerGame():
    game = FarkleDiceGame()
#    game.addPlayer("Louis", "human")
    game.addPlayer("Olivier", "human")
    game.addPlayer("Ordi 1.0")
    game.play()


def main():
    log.basicConfig(format="%(levelname)s: %(message)s", level=50)
    # testCases()
    # randomCheck()
    # playHumanVsComputerGame()
    playComputersGame()


main()
