'''
Created on 26 juil. 2017

@author: irac1
'''
import random
import os
import pickle


def verbose(category, *args):
    verboseFilter = [
        # "evaluateDices",
        # "gameStatistics",
        "AI"
    ]
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
            self.allDicesScoreCombination = 0

        def print(self):
            msg = "max score = " + str(self.maxScore) + "\n"
            msg += "average score per roll = " + str(self.totalScore / self.combination) + "\n"
            msg += "average score per non nul roll = " + \
                repr(self.nonZeroTotalScore / self.nonZeroCombination) + "\n"
            msg += str(self.combination) + " combinations\n"
            msg += str(self.combination - self.nonZeroCombination) + " nul combinations = " + \
                repr(100 * (self.combination - self.nonZeroCombination) / self.combination) + "% \n"
            msg += "Combination with all dices scoring = " + \
                str(self.allDicesScoreCombination) + "\n"
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
                (scoringDices, score) = FarkleDiceGame.evaluateDices(diceRoll + [dice])
                if(len(scoringDices) == len(diceRoll) + 1):
                    # All dices score
                    stats.allDicesScoreCombination += 1
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

    def avgScoreForNbDices(self, nbDices):
        return self.gameStats[nbDices - 1].nonZeroTotalScore / self.gameStats[nbDices - 1].nonZeroCombination

    def computePotentialScore(self, nbDiceToThrow, currentTurnScore):
        # % chance to get non zero combination  = nonZeroCombination / combination
        chanceToGetNonZeroCombination = self.gameStats[nbDiceToThrow -
                                                       1].nonZeroCombination / self.gameStats[nbDiceToThrow - 1].combination
        # average score for non zero combination = nonZeroTotalScore / nonZeroCombination
        avgScoreForNonZeroCombination = self.avgScoreForNbDices(nbDiceToThrow)
        # % chance to get all dices scoring (and rethrow 6 dices) = allDicesScoreCombination / combination
        chanceToGetAllDicesScore = self.gameStats[nbDiceToThrow -
                                                  1].allDicesScoreCombination / self.gameStats[nbDiceToThrow - 1].combination
        # average score for 6 dices rethrow
        avgScoreForNonZero6DicesCombination = self.avgScoreForNbDices(6)
        return chanceToGetNonZeroCombination * (currentTurnScore + avgScoreForNonZeroCombination) + chanceToGetAllDicesScore * avgScoreForNonZero6DicesCombination


class Player:
    def __init__(self, game, name):
        self.name = name
        self.kind = 0
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
        dicesKept.sort()
        self.turnDicesKept += dicesKept + [0]

    def endTurn(self, turnScore, diceRoll):
        if(turnScore):
            if(self.hasStarted or self.turnScore >= FarkleDiceGame.START_SCORE):
                self.score += self.turnScore
                self.hasStarted = True


class ComputerPlayer(Player):
    def __init__(self, game, name="", riskFactor=1.0):
        super().__init__(game, name)
        self.riskFactor = riskFactor
        self.bufferUnderWinScore = 100  # buffer in order not to get too close to Win score to optimize end game
        self.kind = "computer"

    def wantToFollowUp(self, score, nbDices):
        if(self.score + score > FarkleDiceGame.WIN_SCORE - self.bufferUnderWinScore):
            verbose("AI", "AI cannot follow up as score would exceed win score - buffer")
            return False
        potentialScoreIfFollowUp = self.game.gameStats.computePotentialScore(nbDices, score)
        potentialScoreIfStartOver = self.game.gameStats.computePotentialScore(6, 0)
        verbose("AI", "follow-up vs. start over:",
                potentialScoreIfFollowUp, potentialScoreIfStartOver)
        if(potentialScoreIfFollowUp > potentialScoreIfStartOver):
            verbose("AI", "AI decides to follow-up with", score, "points and", nbDices, "dices")
            return True
        else:
            verbose("AI", "AI decides to start over")
            return False

    def __checkIfWorthDiscarding(self, diceRoll, diceKept, remainingDices, potentialScore):
        # TODO: implement another algorithm : list all valid dices combinations
        # and associated potential score, select best combination according to
        # situation (main game, end game)
        if(len(diceKept) == 1):
            # cannot discard anything
            return False
        maxPotentialScore = potentialScore
        diceToDiscard = 0
        # option 1: want to be as close as possible to Win Score - avg score for 6 dices
        # targetScore = FarkleDiceGame.WIN_SCORE - self.score - self.game.gameStats.avgScoreForNbDices(6)
        # option 2: want to be as close as possible to Win Score - buffer
        targetScore = FarkleDiceGame.WIN_SCORE - self.score - self.bufferUnderWinScore
        for dice in diceKept:
            # check what is the best dice to discard and store it in diceToDiscard
            diceKeptDiscarded = list(diceKept)
            diceKeptDiscarded.remove(dice)
            (_, diceScore) = FarkleDiceGame.evaluateDices(diceKeptDiscarded)
            potentialScoreByDiscarding = self.game.gameStats.computePotentialScore(
                remainingDices + 1, diceScore + self.turnScore)
            # check if new score with discard is closer to target score (for end game optimization)
            # option 1 : min distance to target score (can be above target score)
            # if(abs(potentialScoreByDiscarding - targetScore) <= abs(maxPotentialScore - targetScore)):
            # option 2 : closest to target score but under
            if(maxPotentialScore <= potentialScoreByDiscarding <= targetScore):
                maxPotentialScore = potentialScoreByDiscarding
                diceToDiscard = dice
        if (maxPotentialScore > potentialScore):
            # found one dice maximizing potential score
            diceKeptDiscarded = list(diceKept)
            diceKeptDiscarded.remove(diceToDiscard)
            # check if selection still valid
            if(self.game.validPlayerDiceSelection(diceRoll, diceKeptDiscarded, True) is not True):
                return False
            else:
                # proceed with removing dice and recurse to find if more dices are worth discarding
                diceKept.remove(diceToDiscard)
                verbose("AI", "AI checks if worth discarding dice", diceToDiscard)
                newMaxScore = self.__checkIfWorthDiscarding(
                    diceRoll, diceKept, remainingDices + 1, maxPotentialScore)
                if (newMaxScore is not False):
                    maxPotentialScore = newMaxScore
                return maxPotentialScore
        else:
            return False

    def decideNextMove(self, diceRoll):
        (diceKept, diceScore) = FarkleDiceGame.evaluateDices(diceRoll)
        if(not self.hasStarted):
            # not started
            remainingDices = len(diceRoll) - len(diceKept)
            potentialScoreIfContinue = self.game.gameStats.computePotentialScore(
                remainingDices, diceScore + self.turnScore)
            self.__checkIfWorthDiscarding(
                diceRoll, diceKept, remainingDices, potentialScoreIfContinue)
            if(diceScore + self.turnScore < FarkleDiceGame.START_SCORE):
                # keep playing until reach score required for start
                return (True, diceKept)
            else:
                # decides to stop, reset diceKept to keep all dices
                (diceKept, diceScore) = FarkleDiceGame.evaluateDices(diceRoll)
                return (False, diceKept)
        else:
            # started
            if(self.score + self.turnScore + diceScore == FarkleDiceGame.WIN_SCORE):
                # Win : keep all dices & stop
                verbose("AI", "AI scores to win")
                return (False, diceKept)
            # Else: evaluate benefit of continuing
            scoreIfDoNotContinue = diceScore + self.turnScore
            remainingDices = len(diceRoll) - len(diceKept)
            potentialScoreIfContinue = self.game.gameStats.computePotentialScore(
                remainingDices, diceScore + self.turnScore)
            newMaxScore = self.__checkIfWorthDiscarding(
                diceRoll, diceKept, remainingDices, potentialScoreIfContinue)
            if (newMaxScore is not False):
                potentialScoreIfContinue = newMaxScore
            verbose("AI", scoreIfDoNotContinue, potentialScoreIfContinue,
                    self.riskFactor * potentialScoreIfContinue)

            if(self.riskFactor * potentialScoreIfContinue > scoreIfDoNotContinue and self.score + potentialScoreIfContinue < FarkleDiceGame.WIN_SCORE - self.game.gameStats.avgScoreForNbDices(6)):
                # continue if potential score by throwing dices again > current score and
                # does not exceed win score
                verbose("AI", "AI decides to continue")
                return (True, diceKept)

            else:
                # check if reaching end of game
                if(self.score + self.turnScore + diceScore > FarkleDiceGame.WIN_SCORE - self.bufferUnderWinScore):
                    # if score is above Win score - buffer, optimize end game
                    # keep only one 5 or one 1 if possible
                    if(diceKept.count(1) >= 1 and self.score + self.turnScore + FarkleDiceGame.ONE_SCORE <= FarkleDiceGame.WIN_SCORE - self.bufferUnderWinScore):
                        # keep only one 1 if does not exceed win score - buffer
                        verbose("AI", "AI optimizing end game: decides to keep only [1]")
                        diceKept = [1]
                        return (True, diceKept)
                    elif(diceKept.count(5) >= 1):
                        verbose("AI", "AI optimizing end game: decides to keep only [5]")
                        diceKept = [5]
                        return (True, diceKept)
                    else:
                        # abort turn by selecting []
                        verbose("AI", "AI optimizing end game: decides to abort turn to keep win buffer")
                        diceKept = []
                        return (False, diceKept)

                # decides to stop, reset diceKept to keep all dices
                (diceKept, diceScore) = FarkleDiceGame.evaluateDices(diceRoll)
                verbose("AI", "AI decides to score turn")
                return (False, diceKept)


class HumanPlayer(Player):
    def __init__(self, game, name, decideNextMoveUI, wantToFollowUpUI):
        super().__init__(game, name)
        self.decideNextMoveUI = decideNextMoveUI
        self.wantToFollowUpUI = wantToFollowUpUI
        self.kind = "human"

    def wantToFollowUp(self, score, nbDices):
        # returns True/False
        return self.wantToFollowUpUI(score, nbDices)

    def decideNextMove(self, diceRoll):
        # returns (keepPlaying, diceKept)
        return self.decideNextMoveUI(diceRoll)


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

    def addComputerPlayer(self, name, riskFactor=1.0):
        self.players.append(ComputerPlayer(self, name, riskFactor))

    def addHumanPlayer(self, name, decideNextMoveUI, wantToFollowUpUI):
        self.players.append(HumanPlayer(self, name, decideNextMoveUI, wantToFollowUpUI))

    def rollDices(self, nbDices):
        diceRoll = []
        for _ in range(nbDices):
            diceRoll.append(random.choice(FarkleDiceGame.dice))
        return diceRoll

    def validPlayerDiceSelection(self, diceRoll, diceSelection, keepPlaying):
        if(not keepPlaying):
            # Player decides to stop, dice selection must contain all scoring dices or be empty
            (scoringDices, _) = FarkleDiceGame.evaluateDices(diceRoll)
            if(sorted(diceSelection) == sorted(scoringDices) or len(diceSelection) == 0):
                return True
            else:
                return "mustKeepAllScoringDicesToStop"
        else:
            # Player want to continue
            # Selection must not be empty
            if(len(diceSelection) == 0):
                return "invalidDiceSelection"
            # else all dices from selection shall score
            (_, selectionScore) = FarkleDiceGame.evaluateDices(diceSelection)
            selectionValid = True
            for dice in diceSelection:
                selectionMinusDice = list(diceSelection)
                selectionMinusDice.remove(dice)
                (_, selectionMinusDiceScore) = FarkleDiceGame.evaluateDices(selectionMinusDice)
                if(selectionScore == selectionMinusDiceScore):
                    # removing dice did not decrease the score : selection is not valid
                    selectionValid = "invalidDiceSelection"
            return selectionValid

    def play(self):
        gameOver = False
        self.currentPlayer = 0
        scoreForPossibleFollowUp = 0
        nbDicesToThrow = 6
        self.turn = 1
        while(not gameOver):
            self.updateUI(self, "startTurn", self.currentPlayer)
            turnOver = False
            if(scoreForPossibleFollowUp != 0 and self.players[self.currentPlayer].hasStarted and self.players[self.currentPlayer].wantToFollowUp(scoreForPossibleFollowUp, nbDicesToThrow)):
                # check if user want to restart from last player turn score & remaining dices
                self.players[self.currentPlayer].startTurn(scoreForPossibleFollowUp)
                self.updateUI(self, "turnFollowUp", self.currentPlayer, [], [], nbDicesToThrow)
            else:
                nbDicesToThrow = 6
                self.players[self.currentPlayer].startTurn(0)
            while (not turnOver):
                diceRoll = self.rollDices(nbDicesToThrow)
                (_, maxScore) = FarkleDiceGame.evaluateDices(diceRoll)
                if(maxScore == 0):
                    scoreForPossibleFollowUp = 0  # No turn follow-up
                    self.players[self.currentPlayer].endTurn(False, diceRoll)
                    self.updateUI(self, "endTurnBadThrow", self.currentPlayer, diceRoll)
                    turnOver = True
                else:
                    selectionValid = False
                    while(selectionValid is not True):
                        (keepPlaying, diceKept) = self.players[self.currentPlayer].decideNextMove(
                            diceRoll)
                        selectionValid = self.validPlayerDiceSelection(
                            diceRoll, diceKept, keepPlaying)
                        if (selectionValid is not True):
                            self.updateUI(self, selectionValid, self.currentPlayer)
                    (_, turnScore) = FarkleDiceGame.evaluateDices(diceKept)
                    nbDicesToThrow -= len(diceKept)
                    if(nbDicesToThrow <= 0):
                        keepPlaying = True  # must continue if no more dice
                        nbDicesToThrow = 6
                    self.players[self.currentPlayer].addTurnScore(turnScore, diceKept)
                    self.updateUI(self, "PlayerSelectedDices",
                                  self.currentPlayer, diceRoll, diceKept)
                    if(turnScore == 0 or self.players[self.currentPlayer].score + self.players[self.currentPlayer].turnScore > FarkleDiceGame.WIN_SCORE):
                        scoreForPossibleFollowUp = 0  # No turn follow-up
                        self.players[self.currentPlayer].endTurn(False, diceRoll)
                        self.updateUI(self, "endTurnNoScore",
                                      self.currentPlayer, diceRoll, diceKept)
                        turnOver = True
                    elif (not keepPlaying):
                        if(self.players[self.currentPlayer].hasStarted or self.players[self.currentPlayer].turnScore >= FarkleDiceGame.START_SCORE):
                            scoreForPossibleFollowUp = self.players[self.currentPlayer].turnScore
                            self.players[self.currentPlayer].endTurn(True, diceRoll)
                            self.updateUI(self, "endTurnScores",
                                          self.currentPlayer, diceRoll, diceKept)
                        else:
                            scoreForPossibleFollowUp = 0  # No turn follow-up
                            self.players[self.currentPlayer].endTurn(False, diceRoll)
                            self.updateUI(self, "endTurnNoScore",
                                          self.currentPlayer, diceRoll, diceKept)

                        turnOver = True
            if (self.players[self.currentPlayer].score == FarkleDiceGame.WIN_SCORE):
                self.updateUI(self, "gameOver", self.currentPlayer)
                gameOver = True
            self.currentPlayer += 1
            if (self.currentPlayer == len(self.players)):
                self.currentPlayer = 0
                self.turn += 1
        return self.currentPlayer

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
                    # check for additional one or five (sextuplets of ones and fives already
                    # taken care of above)
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
                    # check for additional ones or fives (sextuplets of ones and fives already
                    # taken care of above)
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
                # check for additional fives, additional ones already taken care of by
                # quadruplets, ... above
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
