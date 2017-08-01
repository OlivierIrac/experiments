'''
Created on 26 juil. 2017

@author: irac1
'''
import random
import os
import pickle
from termcolor import cprint

def verbose(category, *args):
    verboseFilter = [  # "evaluateDices",
                    # "gameStatistics",
                    "computerPlayer"
                    ]  # @IgnorePep8
    if(category in verboseFilter):
        print(category, ":", *args)


class GameStatistics:
    class StatisticsPerNbDice:
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

    def __init__(self, forceUpdate=False):
        filename = "gameStatistics.sav"
        if (not forceUpdate and os.path.isfile(filename)):
            # read stats from .sav file
            with open(os.path.join(filename), 'rb') as fp:
                self.gameStats = pickle.load(fp)
            verbose("gameStatistics", "loaded stats from:", filename)
            verbose("gameStatistics", self.print())
        else:
            # compute stats
            self.gameStats = []
            for i in FarkleDiceGame.dice:
                self.gameStats.append(self.__computeStatistics(i))
            verbose("gameStatistics", self.print())
            with open(filename, 'wb') as fp:
                pickle.dump(self.gameStats, fp)
            verbose("gameStatistics", "Saved stats to:", filename)

    def print(self):
        msg = ""
        for i in FarkleDiceGame.dice:
            msg += str(i) + " dices\n" + self.gameStats[i - 1].print()
        return msg

    def __computeStatistics(self, nbDices, diceRoll=[], stats=0, init=True):
        if(init):
            stats = GameStatistics.StatisticsPerNbDice()
        if(nbDices == 1):
            for dice in FarkleDiceGame.dice:
                stats.combination += 1
                (_, score) = FarkleDiceGame.evaluateDices(diceRoll + [dice])
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

    def computePotentialScore(self, nbDiceToThrow, currentTurnScore):
        # % chance to get non zero combination  = nonZeroCombination / combination
        # average score for nbDices = nonZeroTotalScore / nonZeroCombination
        # potential score = % chance to get non zero combination * (currentTurnScore + average score for nbDices)
        # FIXME: take into account probability that all dices can score and result in 6 more dices
        return self.gameStats[nbDiceToThrow - 1].nonZeroCombination / self.gameStats[nbDiceToThrow - 1].combination * (currentTurnScore + self.gameStats[nbDiceToThrow - 1].nonZeroTotalScore / self.gameStats[nbDiceToThrow - 1].nonZeroCombination)


class Player:
    def __init__(self, game, name):
        self.name = name
        self.score = 0
        self.game = game
        self.turnScore = 0
        self.hasStarted = False

    def startTurn(self, turnScore):
        self.turnScore = turnScore
        self.turnDicesKept = []

    def decideNextMove(self, diceRoll):
        raise NotImplementedError()  # pure virtual

    def wantToFollowUp(self, score, nbDices):
        raise NotImplementedError()  # pure virtual

    def addTurnScore(self, score, dicesKept):
        self.turnScore += score
        self.turnDicesKept += dicesKept + [' ']

    def endTurn(self, turnScore, diceRoll):
        if(turnScore):
            if(self.hasStarted or self.turnScore >= FarkleDiceGame.START_SCORE):
                self.score += self.turnScore
                self.hasStarted = True


class ComputerPlayer(Player):
    def __init__(self, game, name="", riskFactor=1.0):
        super().__init__(game, name)
        self.riskFactor = riskFactor

    def wantToFollowUp(self, score, nbDices):
        if(self.score + score > FarkleDiceGame.WIN_SCORE):
            verbose("computerPlayer", "AI cannot follow up as score would exceed win score")
            return False
        potentialScoreIfFollowUp = self.game.gameStats.computePotentialScore(nbDices, score)
        potentialScoreIfStartOver = self.game.gameStats.computePotentialScore(6, 0)
        verbose("computerPlayer", "follow-up vs. start over:", potentialScoreIfFollowUp, potentialScoreIfStartOver)
        if(potentialScoreIfFollowUp > potentialScoreIfStartOver):
            verbose("computerPlayer", "AI decides to follow-up with", score, "points and", nbDices, "dices")
            return True
        else:
            verbose("computerPlayer", "AI decides to start over")
            return False

    def __checkIfWorthDiscarding(self, diceKept, remainingDices, potentialScore):
        if(len(diceKept) == 1):
            # cannot discard anything
            return False
        maxPotentialScore = potentialScore
        diceToDiscard = 0
        for dice in diceKept:
            # create new dice kept list removing dice
            diceKeptDiscarded = list(diceKept)
            diceKeptDiscarded.remove(dice)
            (_, diceScore) = FarkleDiceGame.evaluateDices(diceKeptDiscarded)
            potentialScoreByDiscarding = self.game.gameStats.computePotentialScore(remainingDices + 1, diceScore + self.turnScore)
            if(potentialScoreByDiscarding > maxPotentialScore):
                maxPotentialScore = potentialScoreByDiscarding
                diceToDiscard = dice
        if (maxPotentialScore > potentialScore):
            # found one dice maximizing potential score
            diceKept.remove(diceToDiscard)
            verbose("computerPlayer", "AI decides to discard dice", diceToDiscard)
            newMaxScore = self.__checkIfWorthDiscarding(diceKept, remainingDices + 1, maxPotentialScore)
            if (newMaxScore is not False):
                maxPotentialScore = newMaxScore
            return maxPotentialScore
        else:
            return False

    def decideNextMove(self, diceRoll):
        (diceKept, diceScore) = FarkleDiceGame.evaluateDices(diceRoll)
        if(not self.hasStarted):
            # not started, keep playing until reach score required for start
            remainingDices = len(diceRoll) - len(diceKept)
            potentialScoreIfContinue = self.game.gameStats.computePotentialScore(remainingDices, diceScore + self.turnScore)
            self.__checkIfWorthDiscarding(diceKept, remainingDices, potentialScoreIfContinue)
            if(diceScore + self.turnScore < FarkleDiceGame.START_SCORE):
                # decides to stop, reset diceKept to keep all dices and maximize turnScore
                (diceKept, diceScore) = FarkleDiceGame.evaluateDices(diceRoll)
                return (True, diceKept)
            else:
                return (False, diceKept)
        else:
            # started
            # evaluate benefit of continuing
            scoreIfDoNotContinue = diceScore + self.turnScore
            remainingDices = len(diceRoll) - len(diceKept)
            potentialScoreIfContinue = self.game.gameStats.computePotentialScore(remainingDices, diceScore + self.turnScore)
            newMaxScore = self.__checkIfWorthDiscarding(diceKept, remainingDices, potentialScoreIfContinue)
            if (newMaxScore is not False):
                potentialScoreIfContinue = newMaxScore
            verbose("computerPlayer", scoreIfDoNotContinue, potentialScoreIfContinue, self.riskFactor * potentialScoreIfContinue)
            if(self.riskFactor * potentialScoreIfContinue > scoreIfDoNotContinue and self.score + potentialScoreIfContinue < FarkleDiceGame.WIN_SCORE):
                # continue if potential score by throwing dices again > current score and does not exceed win score
                verbose("computerPlayer", "AI decides to continue")
                return (True, diceKept)
                # TODO: add case of score + scoreIfDoNotContinue > Win score and check if possible to discard to minimize dice score
            else:
                # decides to stop, reset diceKept to keep all dices and maximize turnScore
                (diceKept, diceScore) = FarkleDiceGame.evaluateDices(diceRoll)
                verbose("computerPlayer", "AI decides to stop")
                return (False, diceKept)


class HumanPlayer(Player):
    def __init__(self, game, name=""):
        super().__init__(game, name)

    def wantToFollowUp(self, score, nbDices):
        msg = "Do you want to follow-up on " + str(score) + " points with " + str(nbDices) + " dices? (y/n)"
        key = input(msg)
        if(key == "y"):
            return True
        else:
            return False

    def decideNextMove(self, diceRoll):
        diceKept = []
        diceAvail = list(diceRoll)  # makes a copy
        (diceAllowed, _) = FarkleDiceGame.evaluateDices(diceRoll)
        done = False
        keepPlaying = True
        while(not done):
            # TODO: separate user interaction
            msg = "Select from:" + str(diceAvail) + "(empty to end & continue, anykey for end & stop turn) :"
            dice = input(msg)
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

    def __init__(self, updateUI):
        self.players = []
        self.turn = 0
        self.gameStats = GameStatistics()
        self.updateUI = updateUI
        random.seed()

    @staticmethod
    def __keepOnes(diceRoll, diceKept, score):
        score += FarkleDiceGame.ONE_SCORE * diceRoll.count(1)
        diceKept += [1 for _ in range(diceRoll.count(1))]
        verbose("evaluateDices", diceRoll.count(1), "single ones found")
        return (diceKept, score)

    @staticmethod
    def __keepFives(diceRoll, diceKept, score):
        score += FarkleDiceGame.FIVE_SCORE * diceRoll.count(5)
        diceKept += [5 for _ in range(diceRoll.count(5))]
        verbose("evaluateDices", diceRoll.count(5), "single fives found")
        return (diceKept, score)

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
        scoreForPossibleFollowUp = 0
        nbDicesToThrow = 6
        print(len(self.players), "players:")
        for player in self.players:
            print (player.name)
        self.turn = 1
        while(not gameOver):
            self.updateUI(self, "startTurn", currentPlayer)
            turnOver = False
            if(scoreForPossibleFollowUp != 0 and self.players[currentPlayer].hasStarted and self.players[currentPlayer].wantToFollowUp(scoreForPossibleFollowUp, nbDicesToThrow)):
                # check if user want to restart from last player turn score & remaining dices
                self.players[currentPlayer].startTurn(scoreForPossibleFollowUp)
                self.updateUI(self, "turnFollowUp", currentPlayer, [], [], nbDicesToThrow)
            else:
                nbDicesToThrow = 6
                self.players[currentPlayer].startTurn(0)
            while (not turnOver):
                diceRoll = self.rollDices(nbDicesToThrow)
                (_, maxScore) = FarkleDiceGame.evaluateDices(diceRoll)
                if(maxScore == 0):
                    scoreForPossibleFollowUp = 0  # No turn follow-up
                    self.players[currentPlayer].endTurn(False, diceRoll)
                    self.updateUI(self, "endTurnBadThrow", currentPlayer, diceRoll)
                    turnOver = True
                else:
                    (keepPlaying, diceKept) = self.players[currentPlayer].decideNextMove(diceRoll)
                    (_, turnScore) = FarkleDiceGame.evaluateDices(diceKept)
                    nbDicesToThrow -= len(diceKept)
                    if(nbDicesToThrow <= 0):
                        keepPlaying = True  # must continue if no more dice
                        nbDicesToThrow = 6
                    self.players[currentPlayer].addTurnScore(turnScore, diceKept)
                    self.updateUI(self, "UserSelectedDices", currentPlayer, diceRoll, diceKept)
                    if(turnScore == 0 or self.players[currentPlayer].score + self.players[currentPlayer].turnScore > FarkleDiceGame.WIN_SCORE):
                        scoreForPossibleFollowUp = 0  # No turn follow-up
                        self.players[currentPlayer].endTurn(False, diceRoll)
                        self.updateUI(self, "endTurnNoScore", currentPlayer, diceRoll, diceKept)
                        turnOver = True
                    elif (not keepPlaying):
                        scoreForPossibleFollowUp = self.players[currentPlayer].turnScore
                        self.players[currentPlayer].endTurn(True, diceRoll)
                        self.updateUI(self, "endTurnScores", currentPlayer, diceRoll, diceKept)
                        turnOver = True
            if (self.players[currentPlayer].score == FarkleDiceGame.WIN_SCORE):
                self.updateUI(self, "gameOver", currentPlayer)
                gameOver = True
            currentPlayer += 1
            if (currentPlayer == len(self.players)):
                currentPlayer = 0
                self.turn += 1
        return currentPlayer

    @staticmethod
    def evaluateDices(diceRoll):
        score = 0
        diceKept = []

        if (len(diceRoll) > 6):
            raise ValueError("Too many dices (max 6)!")

        if (len(diceRoll) >= 4):
            # check for dreaded 4 x 2 => 0
            if (diceRoll.count(2) == 4):
                verbose("evaluateDices", "Four twos found")
                return (diceKept, 0)

        if (len(diceRoll) == 6):
            # check for sextuplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 6):
                    verbose("evaluateDices", "Sextuplet found : " + str(i))
                    diceKept = diceRoll
                    return (diceKept, FarkleDiceGame.SEXTUPLET_SCORE)
            # check for straight 1, 2, 3, 4, 5, 6
            straightFound = True
            for i in range(1, 7):
                if (diceRoll.count(i) != 1):
                    straightFound = False
            if (straightFound):
                verbose("evaluateDices", "Straight found")
                diceKept = diceRoll
                return (diceKept, FarkleDiceGame.STRAIGHT_SCORE)

        if (len(diceRoll) >= 5):
            # check for quintuplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 5):
                    verbose("evaluateDices", "Quintuplet found : " + str(i))
                    score = FarkleDiceGame.QUINTUPLET_SCORE
                    diceKept = [x for x in diceRoll if x == i]
                    # check for additional one or five (sextuplets of ones and fives already taken care of above)
                    if (i != 1):
                        (diceKept, score) = FarkleDiceGame.__keepOnes(diceRoll, diceKept, score)
                    if (i != 5):
                        (diceKept, score) = FarkleDiceGame.__keepFives(diceRoll, diceKept, score)

            if (score != 0):
                diceKept.sort()
                return (diceKept, score)

        if (len(diceRoll) >= 4):
            # check for quadruplet
            for i in range(1, 7):
                if (diceRoll.count(i) == 4):
                    verbose("evaluateDices", "Quadruplet found : " + str(i))
                    score = FarkleDiceGame.QUADRUPLET_SCORE
                    diceKept = [x for x in diceRoll if x == i]
                    # check for additional ones or fives (sextuplets of ones and fives already taken care of above)
                    if (i != 1):
                        (diceKept, score) = FarkleDiceGame.__keepOnes(diceRoll, diceKept, score)
                    if (i != 5):
                        (diceKept, score) = FarkleDiceGame.__keepFives(diceRoll, diceKept, score)
            if (score != 0):
                diceKept.sort()
                return (diceKept, score)

        if (len(diceRoll) >= 3):
            # check for three ones
            if (diceRoll.count(1) == 3):
                verbose("evaluateDices", "Three ones found")
                score = FarkleDiceGame.THREE_ONES_SCORE
                diceKept = [1, 1, 1]
                # check for another triplet
                for i in range(2, 7):
                    if (diceRoll.count(i) == 3):
                        verbose("evaluateDices", "Second triplet found : " + str(i))
                        score += FarkleDiceGame.TRIPLETS_BASE_SCORE * i
                        diceKept += [x for x in diceRoll if x == i]
                # check for additional fives, additional ones already taken care of by quadruplets, ... above
                if (score != FarkleDiceGame.THREE_ONES_SCORE + FarkleDiceGame.TRIPLETS_BASE_SCORE * 5):
                    # check for 1 or 2 fives
                    (diceKept, score) = FarkleDiceGame.__keepFives(diceRoll, diceKept, score)
                if (score != 0):
                    diceKept.sort()
                    return (diceKept, score)
            # check for one or two other triplets
            for i in range(2, 7):
                twoTripletsFound = False
                fiveTripletFound = False
                if (diceRoll.count(i) == 3):
                    verbose("evaluateDices", "Triplet found : " + str(i))
                    if (i == 5):
                        fiveTripletFound = True
                    score = FarkleDiceGame.TRIPLETS_BASE_SCORE * i
                    diceKept = [x for x in diceRoll if x == i]
                    for j in range(i + 1, 7):
                        if (diceRoll.count(j) == 3):
                            verbose("evaluateDices", "Second triplet found : " + str(j))
                            twoTripletsFound = True
                            if (j == 5):
                                fiveTripletFound = True
                            score += FarkleDiceGame.TRIPLETS_BASE_SCORE * j
                            diceKept += [x for x in diceRoll if x == j]
                    if (not twoTripletsFound):
                        # check for additional ones & fives
                        (diceKept, score) = FarkleDiceGame.__keepOnes(diceRoll, diceKept, score)
                        if (not fiveTripletFound):
                            (diceKept, score) = FarkleDiceGame.__keepFives(diceRoll, diceKept, score)
                if (score != 0):
                    diceKept.sort()
                    return (diceKept, score)

        # no special combination found, return score for isolated ones and fives
        verbose("evaluateDices", "No combination found")
        (diceKept, score) = FarkleDiceGame.__keepOnes(diceRoll, diceKept, score)
        (diceKept, score) = FarkleDiceGame.__keepFives(diceRoll, diceKept, score)
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

    FarkleDiceGame(updateConsoleUI)
    for diceRoll in testRolls:
        print(diceRoll)
        try:
            print(FarkleDiceGame.evaluateDices(diceRoll))
        except ValueError as e:
            print (e)
        print()


def randomCheck():
    game = FarkleDiceGame(updateConsoleUI)
    for _ in range(20):
        nbDices = random.choice(FarkleDiceGame.dice)
        diceRoll = game.rollDices(nbDices)
        print (diceRoll)
        print (FarkleDiceGame.evaluateDices(diceRoll))
        print()


def updateConsoleUI(game, event, currentPlayer=0, diceRoll=[], dicesKept=[], nbDicesToThrow=0):
    if(event in ["endTurnBadThrow", "endTurnNoScore"]):
        msg = "Bad roll: " + str(diceRoll) + "\n" + game.players[currentPlayer].name + " does not score. Score: " + str(game.players[currentPlayer].score) + " Dices kept:" + str(game.players[currentPlayer].turnDicesKept)
        cprint(msg, 'white', 'on_red')
    elif(event in ["endTurnNoScore"]):
        msg = "Bad roll: " + str(diceRoll)
        print(msg)
        msg = game.players[currentPlayer].name + " does not score. Score: " + str(game.players[currentPlayer].score) + " Dices kept:" + str(game.players[currentPlayer].turnDicesKept)
        cprint(msg, 'white', 'on_red')
    elif(event in ["endTurnScores"]):
        msg = game.players[currentPlayer].name + " scores " + str(game.players[currentPlayer].turnScore) + " points. Score: " + str(game.players[currentPlayer].score) + " Dices kept:" + str(game.players[currentPlayer].turnDicesKept)
        cprint(msg, 'white', 'on_green')
    elif(event in ["startTurn"]):
        msg = game.players[currentPlayer].name + " turn. Score: " + str(game.players[currentPlayer].score)
        cprint(msg, 'white', 'on_blue')
    elif(event in ["turnFollowUp"]):
        msg = game.players[currentPlayer].name + " decides to follow-up with " + str(game.players[currentPlayer].turnScore) + " points and " + str(nbDicesToThrow) + " dices"
        cprint(msg, 'white', 'on_blue')
    elif(event in ["gameOver"]):
        msg = game.players[currentPlayer].name + " wins !"
        cprint(msg, 'white', 'on_cyan', attrs=['blink'])
        print(game.turn, "turns")
        playersByScore = sorted(game.players, key=lambda x: x.score, reverse=True)
        for player in playersByScore:
            print(player.name, player.score)
    else:
        print ("Roll:", diceRoll, "Kept:", dicesKept, "Turn score:", game.players[currentPlayer].turnScore)


def playComputersGame():
    winners = [0 for _ in [x * 0.1 for x in range(5, 20)]]
    for i in range(100):
        game = FarkleDiceGame(updateConsoleUI)
#    game.addPlayer("Louis", "human")
#    game.addPlayer("Olivier", "human")
        for risk in [x * 0.1 for x in range(5, 20)]:
            game.addPlayer("Computer " + str(risk), "computer", risk)
        winner = game.play()
        winners[winner - 1] += 1
        print("Game #", i)
    print(winners)


def playHumanVsComputerGame():
    game = FarkleDiceGame(updateConsoleUI)
#    game.addPlayer("Louis", "human")
    game.addPlayer("Olivier", "human")
    game.addPlayer("Ordi 1.0")
    game.play()


def main():
    # testCases()
    # randomCheck()
    playHumanVsComputerGame()
    # playComputersGame()


main()
