'''
Created on 8 august 2017

@author: irac1
'''

from farkleDiceGame import FarkleDiceGame, GameStatistics
from termcolor import cprint
import random


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
            print(e)
        print()


def randomCheck():
    game = FarkleDiceGame(updateConsoleUI)
    for _ in range(20):
        nbDices = random.choice(FarkleDiceGame.dice)
        diceRoll = game.rollDices(nbDices)
        print(diceRoll)
        print(FarkleDiceGame.evaluateDices(diceRoll))
        print()


def decideNextMoveUI(diceRoll):
    # console UI for human player decide next move
    diceKept = []
    done = False
    keepPlaying = True
    msg = "Dice roll:" + str(diceRoll)
    cprint(msg, 'white', 'on_green')
    print("(1-6, empty to end & continue, anykey for end & stop turn)")
    while(not done):
        dice = input("?")
        if (dice in ['1', '2', '3', '4', '5', '6']):
            diceKept.append(int(dice))
        elif (dice != ''):
            done = True
            keepPlaying = False
        else:
            done = True
    return (keepPlaying, diceKept)


def wantToFollowUpUI(score, nbDices):
    # console UI for human player want to follow up
    msg = "Do you want to follow-up on " + \
        str(score) + " points with " + str(nbDices) + " dices? (y/n)"
    key = input(msg)
    if(key == "y"):
        return True
    else:
        return False


def updateConsoleUI(game, event, currentPlayer=0, diceRoll=[], dicesKept=[], nbDicesToThrow=0):
    if(event in ["endTurnBadThrow"]):
        msg = "Bad roll: " + str(diceRoll)
        cprint(msg, 'white', 'on_red')
        msg = game.players[currentPlayer].name + " end turn. Score: " + \
            str(game.players[currentPlayer].score)
        cprint(msg, 'white', 'on_blue')
    elif(event in ["endTurnNoScore"]):
        msg = "No score"
        cprint(msg, 'white', 'on_red')
        msg = game.players[currentPlayer].name + " end turn. Score: " + \
            str(game.players[currentPlayer].score)
        cprint(msg, 'white', 'on_blue')
    elif(event in ["endTurnScores"]):
        msg = game.players[currentPlayer].name + " end turn. Score: " + \
            str(game.players[currentPlayer].score)
        cprint(msg, 'white', 'on_blue')
    elif(event in ["startTurn"]):
        msg = "\n" + game.players[currentPlayer].name + \
            " turn. Score: " + str(game.players[currentPlayer].score)
        cprint(msg, 'white', 'on_blue')
    elif(event in ["turnFollowUp"]):
        msg = game.players[currentPlayer].name + " decides to follow-up with " + \
            str(game.players[currentPlayer].turnScore) + \
            " points and " + str(nbDicesToThrow) + " dices"
        print(msg)
    elif(event in ["gameOver"]):
        msg = game.players[currentPlayer].name + " wins !"
        cprint(msg, 'white', 'on_green')
        print(game.turn, "turns")
        playersByScore = sorted(game.players, key=lambda x: x.score, reverse=True)
        for player in playersByScore:
            print(player.name, player.score)
    elif(event in ["mustKeepAllScoringDicesToStop"]):
        cprint("You must keep all scoring dices to end turn.", 'white', 'on_red')
    elif(event in ["invalidDiceSelection"]):
        msg = "Invalid dice selection"
        cprint(msg, 'white', 'on_red')
    else:
        print("Roll:", diceRoll, "Kept:", dicesKept,
              "Turn score:", game.players[currentPlayer].turnScore)


def playComputersGame(nbGames=10):
    computersRisk = range(5, 15)
    winners = [0 for _ in [x * 0.1 for x in computersRisk]]
    for i in range(nbGames):
        game = FarkleDiceGame(updateConsoleUI)
        for risk in [x * 0.1 for x in computersRisk]:
            game.addComputerPlayer("Computer " + str(risk), risk)
        winner = game.play()
        winners[winner - 1] += 1
        print("Game #", i)
    print(winners)


def playHumanVsComputerGame():
    game = FarkleDiceGame(updateConsoleUI)
    game.addHumanPlayer("Olivier", decideNextMoveUI, wantToFollowUpUI)
    game.addComputerPlayer("Ordi 1.0")
    game.addComputerPlayer("Ordi 0.9", 0.9)
    game.play()


def main():
    # testCases()
    # randomCheck()
    playHumanVsComputerGame()
    # playComputersGame(100)


main()
