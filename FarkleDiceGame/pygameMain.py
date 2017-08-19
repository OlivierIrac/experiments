'''
Created on 10 august 2017

@author: irac1
'''

import os
from farkleDiceGame import FarkleDiceGame, GameStatistics
from pygameUI import *


def playGame():
    UI = FarklePygameUI()
    game = FarkleDiceGame(UI.updatePygameUI)
    game.addComputerPlayer("Computer")
    game.addComputerPlayer("Cautious Computer", 0.7)
    game.addComputerPlayer("Risk Computer", 1.3)
    game.addHumanPlayer("Olivier", UI.decideNextMoveUI, UI.wantToFollowUpUI)
    game.play()


class FarklePygameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((660, 240))
        pygame.display.set_caption('Farkle Dice Game')
        self.clock = pygame.time.Clock()
        self.diceRollAnimationEvent = 0
        self.diceKeptUpdateEvent = pygame.USEREVENT + 1
        self.animationTime = 300
        self.thinkTime = 400  # Animation pause time after dice roll for computer to "think"
        self.diceRoll = []
        self.game = 0
        self.currentPlayer = 0
        self.keepPlaying = False
        self.previousUserSelectionValid = True

        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 160, 0))

        # Creates the UI objects
        self.UIObjects = []

        self.infoBox = MsgBoxUI("", pygame.Color('black'), pygame.Color(
            'white'), 400, 30, 16, (10, 10), self.screen)
        self.UIObjects.append(self.infoBox)

        self.endAnimationMsg = ""
        self.endAnimationSound = False
        self.turnInfoBox = MsgBoxUI("", pygame.Color('black'), pygame.Color(
            'white'), 400, 30, 16, (10, 50), self.screen)
        self.UIObjects.append(self.turnInfoBox)

        self.scoreBox = MsgBoxUI("", pygame.Color('black'), pygame.Color(
            'white'), 230, 140, 16, (420, 10), self.screen)
        self.UIObjects.append(self.scoreBox)

        self.dicesColor = (240, 240, 240)
        self.diceRollUI = DiceRollUI([], 10, 50, (10, 100), self.screen,
                                     self.dicesColor, False, self.animationTime)
        self.UIObjects.append(self.diceRollUI)

        self.turnDiceKept = []
        self.dicesKept = []
        self.diceKeptAnimationStep = 0
        self.dicesKeptAnimation = []
        self.turnDiceKeptUI = DiceRollUI([], 5, 30, (10, 160), self.screen)
        self.UIObjects.append(self.turnDiceKeptUI)

        self.buttonContinue = ButtonUI("Continue", pygame.Color(
            'white'), pygame.Color('green'), 0, 0, (10, 200), self.screen)
        self.UIObjects.append(self.buttonContinue)

        self.buttonStop = ButtonUI("Stop", pygame.Color(
            'white'), pygame.Color('red'), 0, 0, (100, 200), self.screen)
        self.UIObjects.append(self.buttonStop)
        self.buttonStop.hide()

        # load sounds
        self.keepDiceSound = pygame.mixer.Sound(os.path.join("data", "334764__dneproman__ma-sfx-8bit-tech-gui-9.wav"))
        self.badSound = pygame.mixer.Sound(os.path.join("data", "242503__gabrielaraujo__failure-wrong-action.wav"))
        self.goodSound = pygame.mixer.Sound(os.path.join("data", "345299__scrampunk__okay.wav"))
        self.diceSound = pygame.mixer.Sound(os.path.join("data", "276534__kwahmah-02__cokecan17.wav"))
        self.wrongSelectionSound = pygame.mixer.Sound(os.path.join("data", "142608__autistic-lucario__error.wav"))
        self.winSound = pygame.mixer.Sound(os.path.join("data", "253177__suntemple__retro-accomplished-sfx.wav"))

    def startDiceAnimation(self, msg, sound=False, selectable=False):
        self.diceRollUI.update(self.diceRoll, self.dicesColor, selectable, self.animationTime)
        self.diceRollAnimationEvent = self.diceRollUI.startAnimation()
        self.diceKeptAnimationStep = 0
        self.dicesKeptAnimation = list(self.turnDiceKept)
        self.diceAnimationRunning = True
        pygame.time.set_timer(self.diceKeptUpdateEvent,
                              self.animationTime * len(self.diceRoll) + self.thinkTime)
        self.endAnimationMsg = msg
        self.endAnimationSound = sound
        self.turnInfoBox.update("Rolling dices...")

    def completeDiceAnimation(self):
        # fast forward all on-going animations
        self.diceRollAnimationEvent = self.diceRollUI.stopAnimation()
        for n in range(self.diceKeptAnimationStep, len(self.dicesKept)):
            self.diceRoll.remove(self.dicesKept[n])
        self.diceRollUI.update(self.diceRoll)
        self.diceKeptAnimationStep = len(self.dicesKept)
        # set short timer to manage end of animation update
        pygame.time.set_timer(self.diceKeptUpdateEvent, 1)

    def stopDiceAnimation(self):
        # stop all on-going animations
        self.diceRollAnimationEvent = self.diceRollUI.stopAnimation()
        pygame.time.set_timer(self.diceKeptUpdateEvent, 0)
        self.diceAnimationRunning = False

    def decideNextMoveUI(self, diceRoll):
        # UI for human player dice selection and stop/continue
        self.diceRoll = diceRoll
        self.dicesKept = []
        if(self.previousUserSelectionValid):
            # animate dice roll
            msg = "Select dices. Turn score : " + str(self.game.players[self.currentPlayer].turnScore)
            self.startDiceAnimation(msg, 0, True)
        # else keep current dice roll and wait new selection
        self.buttonStop.show()
        self.UIMainLoop(False)
        self.buttonStop.hide()
        self.previousUserSelectionValid = True
        return(self.keepPlaying, self.dicesKept)

    def wantToFollowUpUI(self, score, nbDices):
        # UI for human player want to follow up
        msg = "Do you want to continue with " + \
            str(score) + " points and " + str(nbDices) + " dices?"
        self.turnInfoBox.update(msg)
        self.buttonStop.show()
        self.UIMainLoop(False)
        self.buttonStop.hide()
        return self.keepPlaying

    def updatePygameUI(self, game, gameEvent, currentPlayer, diceRoll=[], dicesKept=[], nbDicesToThrow=0):
        self.dicesKept = dicesKept
        self.diceRoll = diceRoll
        self.game = game
        self.currentPlayer = currentPlayer

        # update score box
        msg = ""
        playersByScore = sorted(game.players, key=lambda x: x.score, reverse=True)
        for player in playersByScore:
            msg += player.name + " : " + str(player.score) + "\n"
        self.scoreBox.update(msg)

        # update info box
        msg = "Turn # " + str(game.turn) + " - " + game.players[currentPlayer].name
        self.infoBox.update(msg)

        done = False
        # process Farkle Game events
        # updates infoBox, diceroll, dicekept UI elements, starts animations
        if(gameEvent in ["endTurnBadThrow"]):
            self.startDiceAnimation("End turn : bad roll!", self.badSound)
        elif(gameEvent in ["endTurnNoScore"]):
            self.stopDiceAnimation()
            self.turnInfoBox.update("End turn : No score !")
            self.badSound.play()
        elif(gameEvent in ["endTurnScores"]):
            self.stopDiceAnimation()
            self.diceRollUI.update([])
            msg = 'End turn : ' + str(game.players[currentPlayer].turnScore)
            self.turnInfoBox.update(msg)
            self.goodSound.play()
        elif(gameEvent in ["startTurn"]):
            self.turnDiceKept = []
            self.turnDiceKeptUI.update([])
            self.turnInfoBox.update('Start turn')
            self.diceRollUI.update(self.diceRoll)
            done = True
        elif(gameEvent in ["turnFollowUp"]):
            self.stopDiceAnimation()
            self.turnDiceKeptUI.update([])
            if(game.players[currentPlayer].kind == "computer"):
                msg = game.players[currentPlayer].name + " decides to follow-up with " + \
                    str(game.players[currentPlayer].turnScore) + \
                    " points and " + str(nbDicesToThrow) + " dices"
                self.turnInfoBox.update(msg)
            else:
                done = True
        elif(gameEvent in ["gameOver"]):
            self.diceRollUI.update([])
            self.stopDiceAnimation()
            msg = "Game over : " + game.players[currentPlayer].name + " wins !"
            self.turnInfoBox.update(msg)
            self.winSound.play()
        elif(gameEvent in ["mustKeepAllScoringDicesToStop"]):
            self.stopDiceAnimation()
            self.turnInfoBox.update("You must keep all scoring dices to end turn.")
            self.wrongSelectionSound.play()
            self.previousUserSelectionValid = False
            done = True
        elif(gameEvent in ["invalidDiceSelection"]):
            self.stopDiceAnimation()
            self.turnInfoBox.update("Invalid dice selection")
            self.wrongSelectionSound.play()
            self.previousUserSelectionValid = False
            done = True
        elif(gameEvent in "PlayerSelectedDices"):
            if(game.players[currentPlayer].kind == "computer"):
                msg = "Turn score : " + str(game.players[currentPlayer].turnScore)
                self.startDiceAnimation(msg, False, False)
            else:
                self.turnDiceKept = list(self.game.players[self.currentPlayer].turnDicesKept)
                self.turnDiceKeptUI.update(self.turnDiceKept)
                done = True
        else:
            print("Invalid game event")

        self.UIMainLoop(done)

    def UIMainLoop(self, done):
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
                    if(objectEvent == "buttonPressed"):
                        if(self.diceAnimationRunning):
                            self.completeDiceAnimation()
                        else:
                            self.dicesKept = self.diceRollUI.getDiceSelection()
                            if(UIObject == self.buttonContinue):
                                self.keepPlaying = True
                            elif(UIObject == self.buttonStop):
                                self.keepPlaying = False
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
                self.diceSound.play()
                self.diceRollUI.updateAnimation()

            if(event.type == self.diceKeptUpdateEvent):
                # Animate dice kept
                if(self.diceAnimationRunning):
                    if (self.diceKeptAnimationStep >= len(self.dicesKept)):
                        # reached the end of animation
                        self.turnInfoBox.update(self.endAnimationMsg)
                        self.turnDiceKept = list(self.game.players[self.currentPlayer].turnDicesKept)
                        self.turnDiceKeptUI.update(self.turnDiceKept)
                        self.stopDiceAnimation()
                        if(self.endAnimationSound):
                            self.endAnimationSound.play()
                    else:
                        # remove one by one, dices kept from dice roll
                        self.diceRoll.remove(self.dicesKept[self.diceKeptAnimationStep])
                        self.diceRollUI.update(self.diceRoll)
                        # add one by one, dices kept to turn dice kept
                        self.dicesKeptAnimation.append(self.dicesKept[self.diceKeptAnimationStep])
                        self.turnDiceKeptUI.update(self.dicesKeptAnimation)
                        pygame.time.set_timer(self.diceKeptUpdateEvent, self.animationTime)
                        self.keepDiceSound.play()
                        self.diceKeptAnimationStep += 1


playGame()
