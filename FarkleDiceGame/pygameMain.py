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
    # game.addPlayer("Margot", "human")
    # game.addPlayer("Louis", "human")
    # game.addPlayer("Olivier", "human")
    game.addComputerPlayer("Ordi 1.0")
    game.addComputerPlayer("Ordi 0.9", 0.9)
    game.play()


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


class FarklePygameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()
        self.diceRollAnimationEvent = 0
        self.diceKeptUpdateEvent = pygame.USEREVENT + 1
        self.animationTime = 300
        self.thinkTime = 400  # Animation pause time after dice roll for computer to "think"
        self.diceRoll = []

        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 160, 0))

        # Creates the UI objects
        self.UIObjects = []

        self.infoBox = MsgBoxUI("", pygame.Color('black'), pygame.Color(
            'white'), 480, 30, 16, (10, 10), self.screen)
        self.UIObjects.append(self.infoBox)

        self.endAnimationMsg = ""
        self.endAnimationSound = False
        self.turnInfoBox = MsgBoxUI("", pygame.Color('black'), pygame.Color(
            'white'), 480, 30, 16, (10, 50), self.screen)
        self.UIObjects.append(self.turnInfoBox)

        self.scoreBox = MsgBoxUI("", pygame.Color('black'), pygame.Color(
            'white'), 150, 70, 16, (500, 10), self.screen)
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
            'white'), pygame.Color('green'), 0, 0, (10, 200), self.screen)
        self.UIObjects.append(self.buttonStopTurn)
        
        # load sounds
        self.keepDiceSound = pygame.mixer.Sound("334764__dneproman__ma-sfx-8bit-tech-gui-9.wav")
        self.badSound = pygame.mixer.Sound("382310__myfox14__game-over-arcade.wav")
        self.goodSound = pygame.mixer.Sound("368691__fartbiscuit1700__8-bit-arcade-video-game-start-sound-effect-gun-reload-and-jump.wav")


    def startDiceAnimation(self, msg, sound=False):
        self.diceRollUI.update(self.diceRoll, pygame.Color('white'), False, self.animationTime)
        self.diceRollAnimationEvent = self.diceRollUI.startAnimation()
        self.diceKeptAnimationStep = 0
        self.dicesKeptAnimation = list(self.turnDiceKept)
        self.diceAnimationRunning = True
        pygame.time.set_timer(self.diceKeptUpdateEvent,
                              self.animationTime * len(self.diceRoll) + self.thinkTime)
        self.endAnimationMsg = msg
        self.endAnimationSound = sound
        self.turnInfoBox.update("Rolling dices and thinking ...")

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
            msg = game.players[currentPlayer].name + " decides to follow-up with " + \
                str(game.players[currentPlayer].turnScore) + \
                " points and " + str(nbDicesToThrow) + " dices"
            self.turnInfoBox.update(msg)
        elif(gameEvent in ["gameOver"]):
            self.diceRollUI.update([])
            self.stopDiceAnimation()
            msg = "Game over : " + game.players[currentPlayer].name + " wins !"
            self.turnInfoBox.update(msg)
        elif(gameEvent in ["mustKeepAllScoringDicesToStop"]):
            self.stopDiceAnimation()
            self.turnInfoBox.update("You must keep all scoring dices to end turn.")
        elif(gameEvent in ["invalidDiceSelection"]):
            self.stopDiceAnimation()
            self.turnInfoBox.update("Invalid dice selection")
        elif(gameEvent in "PlayerSelectedDices"):
            msg = "Turn score : " + str(game.players[currentPlayer].turnScore)
            self.startDiceAnimation(msg)
        else:
            print("Invalid game event")
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
                        self.turnInfoBox.update(self.endAnimationMsg)
                        self.turnDiceKept = list(game.players[currentPlayer].turnDicesKept)
                        self.turnDiceKeptUI.update(self.turnDiceKept)
                        self.stopDiceAnimation()
                        if(self.endAnimationSound):
                            self.endAnimationSound.play()
                        # done = True
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
