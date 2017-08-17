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
        self.diceRollAnimationEvent = 0
        self.diceKeptUpdateEvent = pygame.USEREVENT + 1
        self.animationTime = 500
        self.diceRoll = []

        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 160, 0))

        # Creates the UI objects
        self.UIObjects = []

        self.infoBox = MsgBoxUI("", pygame.Color('white'), pygame.Color(
            'blue'), 480, 30, 16, (10, 10), self.screen)
        self.UIObjects.append(self.infoBox)

        self.endAnimationMsg = ""
        self.turnInfoBox = MsgBoxUI("", pygame.Color('white'), pygame.Color(
            'blue'), 480, 30, 16, (10, 50), self.screen)
        self.UIObjects.append(self.turnInfoBox)

        self.scoreBox = MsgBoxUI("", pygame.Color('white'), pygame.Color(
            'blue'), 150, 70, 16, (500, 10), self.screen)
        self.UIObjects.append(self.scoreBox)

        self.diceRollUI = DiceRollUI([], 10, 50, (10, 100), self.screen,
                                     pygame.Color('white'), False, self.animationTime)
        self.UIObjects.append(self.diceRollUI)

        self.turnDiceKept = []
        self.dicesKept = []
        self.diceKeptAnimationStep = 0
        self.dicesKeptAnimation = []
        self.turnDiceKeptUI = DiceRollUI([], 10, 30, (10, 160), self.screen)
        self.UIObjects.append(self.turnDiceKeptUI)

        self.buttonStopTurn = ButtonUI("Next", pygame.Color(
            'white'), pygame.Color('blue'), 0, 16, (10, 200), self.screen)
        self.UIObjects.append(self.buttonStopTurn)

    def startDiceAnimation(self, msg):
        self.diceRollUI.update(self.diceRoll, pygame.Color('white'), False, self.animationTime)
        self.diceRollAnimationEvent = self.diceRollUI.startAnimation()
        self.diceKeptAnimationStep = 0
        self.dicesKeptAnimation = list(self.turnDiceKept)
        self.diceAnimationRunning = True
        pygame.time.set_timer(self.diceKeptUpdateEvent,
                              self.animationTime * len(self.diceRoll) + self.animationTime)
        self.endAnimationMsg = msg

    def completeDiceAnimation(self):
        # fast forward all on-going animations
        self.diceRollAnimationEvent = self.diceRollUI.stopAnimation()
        pygame.time.set_timer(self.diceKeptUpdateEvent, 1)
        self.diceKeptAnimationStep = len(self.dicesKept)

    def stopDiceAnimation(self):
        # stop all on-going animations
        self.diceRollAnimationEvent = self.diceRollUI.stopAnimation()
        pygame.time.set_timer(self.diceKeptUpdateEvent, 0)
        self.diceAnimationRunning = False

    def updatePygameUI(self, game, gameEvent, currentPlayer=0, diceRoll=[], dicesKept=[], nbDicesToThrow=0):
        self.dicesKept = dicesKept
        self.diceRoll = diceRoll

        # update score box
        msg = ""
        playersByScore = sorted(game.players, key=lambda x: x.score, reverse=True)
        for player in playersByScore:
            msg += player.name + " " + str(player.score) + "\n"
        self.scoreBox.update(msg)

        # update info box
        msg = "Turn # " + str(game.turn) + " " + game.players[currentPlayer].name
        self.infoBox.update(msg)

        done = False
        # process Farkle Game events
        # updates infoBox, diceroll, dicekept UI elements, starts animations
        if(gameEvent in ["endTurnBadThrow"]):
            self.startDiceAnimation("End turn : bad roll!")
        elif(gameEvent in ["endTurnNoScore"]):
            self.stopDiceAnimation()
            self.turnInfoBox.update("End turn : No score !")
        elif(gameEvent in ["endTurnScores"]):
            self.stopDiceAnimation()
            msg = 'End turn : ' + str(game.players[currentPlayer].turnScore)
            self.turnInfoBox.update(msg)
        elif(gameEvent in ["startTurn"]):
            self.turnDiceKept = []
            self.turnDiceKeptUI.update([])
            self.turnInfoBox.update('Start turn')
            self.diceRollUI.update(self.diceRoll)
            done = True
        elif(gameEvent in ["turnFollowUp"]):
            self.stopDiceAnimation()
            self.turnDiceKeptUI.update([])
            msg = game.players[currentPlayer].name + " decides to follow-up with " + \
                str(game.players[currentPlayer].turnScore) + \
                " points and " + str(nbDicesToThrow) + " dices"
            self.turnInfoBox.update(msg)
        elif(gameEvent in ["gameOver"]):
            self.stopDiceAnimation()
            msg = "Game over : " + game.players[currentPlayer].name + " wins !"
            self.turnInfoBox.update(msg)
        elif(gameEvent in ["mustKeepAllScoringDicesToStop"]):
            self.stopDiceAnimation()
            self.turnInfoBox.update("You must keep all scoring dices to end turn.")
        elif(gameEvent in ["invalidDiceSelection"]):
            self.stopDiceAnimation()
            self.turnInfoBox.update("Invalid dice selection")
        else:
            msg = "Turn score : " + str(game.players[currentPlayer].turnScore)
            self.startDiceAnimation(msg)

        while(not done):
            # draw UI
            self.screen.blit(self.background, (0, 0))
            for UIObject in self.UIObjects:
                UIObject.draw()
            pygame.display.flip()

            # process mouse and keyboards events
            event = pygame.event.poll()
            for UIObject in self.UIObjects:
                objectEvent = UIObject.handleEvent(event)
                if(objectEvent):
                    if(UIObject == self.buttonStopTurn and objectEvent == "buttonPressed"):
                        if(self.diceAnimationRunning):
                            self.completeDiceAnimation()
                        else:
                            done = True

            if(event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()

            if(event.type == pygame.KEYDOWN):
                if(self.diceAnimationRunning):
                    self.completeDiceAnimation()
                else:
                    done = True

            # process animation timer events
            if(event.type == self.diceRollAnimationEvent):
                # Animate dice roll throw
                self.diceRollUI.updateAnimation()

            if(event.type == self.diceKeptUpdateEvent):
                # Animate dice kept
                if(self.diceAnimationRunning):
                    if (self.diceKeptAnimationStep >= len(self.dicesKept)):
                        # reached the end of animation
                        print("eof of dice animation")
                        self.turnInfoBox.update(self.endAnimationMsg)
                        self.turnDiceKept = list(game.players[currentPlayer].turnDicesKept)
                        self.turnDiceKeptUI.update(self.turnDiceKept)
                        self.stopDiceAnimation()
                        # done = True
                    else:
                        # remove one by one, dices kept from dice roll
                        self.diceRoll.remove(self.dicesKept[self.diceKeptAnimationStep])
                        self.diceRollUI.update(self.diceRoll)
                        # add one by one, dices kept to turn dice kept
                        self.dicesKeptAnimation.append(self.dicesKept[self.diceKeptAnimationStep])
                        self.turnDiceKeptUI.update(self.dicesKeptAnimation)
                        pygame.time.set_timer(self.diceKeptUpdateEvent, self.animationTime)
                        self.diceKeptAnimationStep += 1


playGame()
