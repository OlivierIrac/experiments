'''
Created on 10 août 2017

@author: irac1
'''

from farkleDiceGame import FarkleDiceGame, GameStatistics
from pygameUI import *


def playGame():
    game = FarkleDiceGame(updatePygameUI)
    # game.addPlayer("Margot", "human")
    # game.addPlayer("Louis", "human")
    game.addPlayer("Olivier", "human")
    game.addPlayer("Ordi 1.0")
    game.addPlayer("Ordi 0.9", "computer", 0.9)
    game.play()


class FarklePygameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.clock = pygame.time.Clock()

        # Create The Backgound
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 160, 0))

        self.UIObjects = []

        # TODO: create static objects
        # msg box
        # buttons?
        # diceroll ?
        # dicekept ?
        # players and score
        # turns
        # player turn

        buttonStopTurn = ButtonUI("Stop turn and score",
                                  pygame.Color('blue'), 0, 20, (10, 400), screen)
        UIObjects.append(buttonStopTurn)
        buttonKeepDicesAndThrow = ButtonUI(
            "Keep selected dices and throw",  pygame.Color('cyan'), 0, 20, (300, 400), screen)

    def updatePygameUI(self, game, gameEvent, currentPlayer=0, diceRoll=[], dicesKept=[], nbDicesToThrow=0):
        if(gameEvent in ["endTurnBadThrow"]):
            msg = "Bad roll: " + str(diceRoll)
            cprint(msg, 'white', 'on_red')
            msg = game.players[currentPlayer].name + " end turn. Score: " + \
                str(game.players[currentPlayer].score)
            cprint(msg, 'white', 'on_blue')
        elif(gameEvent in ["endTurnNoScore"]):
            msg = "No score"
            cprint(msg, 'white', 'on_red')
            msg = game.players[currentPlayer].name + " end turn. Score: " + \
                str(game.players[currentPlayer].score)
            cprint(msg, 'white', 'on_blue')
        elif(gameEvent in ["endTurnScores"]):
            msg = game.players[currentPlayer].name + " end turn. Score: " + \
                str(game.players[currentPlayer].score)
            cprint(msg, 'white', 'on_blue')
        elif(gameEvent in ["startTurn"]):
            msg = "\n" + game.players[currentPlayer].name + \
                " turn. Score: " + str(game.players[currentPlayer].score)
            cprint(msg, 'white', 'on_blue')
        elif(gameEvent in ["turnFollowUp"]):
            msg = game.players[currentPlayer].name + " decides to follow-up with " + \
                str(game.players[currentPlayer].turnScore) + \
                " points and " + str(nbDicesToThrow) + " dices"
            print(msg)
        elif(gameEvent in ["gameOver"]):
            msg = game.players[currentPlayer].name + " wins !"
            cprint(msg, 'white', 'on_green')
            print(game.turn, "turns")
            playersByScore = sorted(game.players, key=lambda x: x.score, reverse=True)
            for player in playersByScore:
                print(player.name, player.score)
        elif(gameEvent in ["mustKeepAllScoringDicesToStop"]):
            cprint("You must keep all scoring dices to end turn.", 'white', 'on_red')
        elif(gameEvent in ["invalidDiceSelection"]):
            msg = "Invalid dice selection"
            cprint(msg, 'white', 'on_red')
        else:
            print("Roll:", diceRoll, "Kept:", dicesKept,
                  "Turn score:", game.players[currentPlayer].turnScore)


done = False
while (not done):
    pygame.display.set_caption(" FPS : {:.4}".format(clock.get_fps()))
    event = pygame.event.poll()

    if (event.type == pygame.QUIT):
        done = True
    if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        done = True

    screen.blit(background, (0, 0))

    for UIObject in UIObjects:
        objectEvent = UIObject.handleEvent(event)
        UIObject.draw()
        if(objectEvent):
            print(objectEvent)

    pygame.display.flip()
    clock.tick(120)
