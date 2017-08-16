'''
Created on 10 august 2017

@author: irac1
'''

from farkleDiceGame import FarkleDiceGame, GameStatistics
from pygameUI import *


def playGame():
    UI = FarklePygameUI()
    game = FarkleDiceGame(UI.updatePygameUI)
    # game.addPlayer("Margot", "human")
    # game.addPlayer("Louis", "human")
    # game.addPlayer("Olivier", "human")
    game.addPlayer("Ordi 1.0")
    game.addPlayer("Ordi 0.9", "computer", 0.9)
    game.play()


class FarklePygameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.animationEvent = 0
        self.diceKeptUpdateEvent = pygame.USEREVENT + 1
        self.animationTime = 500

        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 160, 0))

        self.UIObjects = []

        self.infoBox = MsgBoxUI("", pygame.Color('white'), pygame.Color(
            'blue'), 480, 30, 16, (10, 10), self.screen)
        self.UIObjects.append(self.infoBox)

        self.animationEndTurnInfo = ""
        self.turnInfoBox = MsgBoxUI("", pygame.Color('white'), pygame.Color(
            'blue'), 480, 30, 16, (10, 50), self.screen)
        self.UIObjects.append(self.turnInfoBox)

        self.scoreBox = MsgBoxUI("", pygame.Color('white'), pygame.Color(
            'blue'), 150, 70, 16, (500, 10), self.screen)
        self.UIObjects.append(self.scoreBox)

        self.diceRollUI = DiceRollUI([], 10, 50, (10, 100), self.screen,
                                     pygame.Color('white'), False, self.animationTime)
        self.UIObjects.append(self.diceRollUI)

        self.diceKept = []
        self.diceKeptUI = DiceRollUI([], 10, 30, (10, 160), self.screen)
        self.UIObjects.append(self.diceKeptUI)

        self.buttonStopTurn = ButtonUI("Next turn", pygame.Color(
            'white'), pygame.Color('blue'), 0, 12, (10, 400), self.screen)
        self.UIObjects.append(self.buttonStopTurn)

        self.buttonKeepDicesAndThrow = ButtonUI(
            "Keep dices and throw again", pygame.Color('white'), pygame.Color('cyan'), 0, 12, (300, 400), self.screen)
        self.UIObjects.append(self.buttonKeepDicesAndThrow)

    def updatePygameUI(self, game, gameEvent, currentPlayer=0, diceRoll=[], dicesKept=[], nbDicesToThrow=0):
        msg = ""
        playersByScore = sorted(game.players, key=lambda x: x.score, reverse=True)
        for player in playersByScore:
            msg += player.name + " " + str(player.score) + "\n"
        self.scoreBox.update(msg)

        msg = "Turn # " + str(game.turn) + " " + game.players[currentPlayer].name
        self.infoBox.update(msg)

        done = False

        if(gameEvent in ["endTurnBadThrow"]):
            self.diceRollUI.update(diceRoll, pygame.Color('red'), False, self.animationTime)
            self.animationEvent = self.diceRollUI.startAnimation()
            self.animationEndTurnInfo = "End turn : bad roll!"
        elif(gameEvent in ["endTurnNoScore"]):
            self.diceRollUI.update(diceRoll, pygame.Color('white'), False, self.animationTime)
            self.animationEvent = self.diceRollUI.startAnimation()
            self.animationEndTurnInfo = "End turn : No score !"
        elif(gameEvent in ["endTurnScores"]):
            self.diceRollUI.update(diceRoll, pygame.Color('white'), False, 0)
            msg = 'End turn : ' + str(game.players[currentPlayer].turnScore)
            self.turnInfoBox.update(msg)
        elif(gameEvent in ["startTurn"]):
            self.diceKept = []
            self.diceKeptUI.update([])
            self.turnInfoBox.update('Start turn')
            self.diceRollUI.update(diceRoll, pygame.Color('white'), False, 0)
            done = True
        elif(gameEvent in ["turnFollowUp"]):
            self.diceKeptUI.update([])
            self.turnInfoBox.update("")
            msg = game.players[currentPlayer].name + " decides to follow-up with " + \
                str(game.players[currentPlayer].turnScore) + \
                " points and " + str(nbDicesToThrow) + " dices"
            self.turnInfoBox.update(msg)
        elif(gameEvent in ["gameOver"]):
            msg = "Game over : " + game.players[currentPlayer].name + " wins !"
            playersByScore = sorted(game.players, key=lambda x: x.score, reverse=True)
            for player in playersByScore:
                msg += player.name + str(player.score)
            self.turnInfoBox.update(msg)
        elif(gameEvent in ["mustKeepAllScoringDicesToStop"]):
            self.turnInfoBox.update("You must keep all scoring dices to end turn.")
        elif(gameEvent in ["invalidDiceSelection"]):
            self.turnInfoBox.update("Invalid dice selection")
        else:
            self.diceRollUI.update(diceRoll, pygame.Color('white'), False, self.animationTime)
            self.animationEvent = self.diceRollUI.startAnimation()
            pygame.time.set_timer(self.diceKeptUpdateEvent,
                                  self.animationTime * len(diceRoll) + 2000)

        while(not done):
            self.screen.blit(self.background, (0, 0))
            for UIObject in self.UIObjects:
                UIObject.draw()
            pygame.display.flip()

            event = pygame.event.poll()
            for UIObject in self.UIObjects:
                objectEvent = UIObject.handleEvent(event)
                if(objectEvent):
                    if(UIObject == self.buttonStopTurn and objectEvent == "buttonPressed"):
                        done = True

            if (event.type == self.animationEvent):
                self.diceRollUI.updateAnimation()
                if(self.diceRollUI.isAnimationComplete()):
                    self.turnInfoBox.update(self.animationEndTurnInfo)
                    self.animationEndTurnInfo = ""

            if (event.type == self.diceKeptUpdateEvent):
                self.diceKept = game.players[currentPlayer].turnDicesKept
                self.diceKeptUI.update(self.diceKept)
                msg = "Turn score : " + str(game.players[currentPlayer].turnScore)
                self.turnInfoBox.update(msg)
                pygame.time.set_timer(self.diceKeptUpdateEvent, 0)
                done = True

            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                else:
                    done = True

        # complete all on-going animations
        # FIXME: not working, UI is out of sync
        self.animationEvent = self.diceRollUI.stopAnimation()
        pygame.time.set_timer(self.diceKeptUpdateEvent, 1)


playGame()
