'''
Created on 8 august 2017

@author: irac1
'''

import pygame
import random
from threading import Timer


class Dice:

    def __init__(self, diceValue, size, position):
        self.diceValue = diceValue
        self.backgroundColor = (255, 255, 255)
        self.borderColor = (0, 0, 0)
        self.dotColor = (0, 0, 0)
        self.borderThickness = 1
        self.size = size
        self.position = position
        self.dotSize = int(self.size / 10)
        self.margin = int(self.size / 4)
        self.center = int(self.size / 2)
        self.outMargin = self.size - self.margin
        self.dotPosition = [
            [
                (self.center, self.center)  # 1
            ],
            [
                (self.margin, self.margin), (self.outMargin, self.outMargin)  # 2
            ],
            [
                (self.margin, self.margin), (self.center, self.center),
                (self.outMargin, self.outMargin)  # 3
            ],
            [
                (self.margin, self.margin), (self.outMargin, self.outMargin),
                (self.margin, self.outMargin), (self.outMargin, self.margin)  # 4
            ],
            [
                (self.margin, self.margin), (self.outMargin, self.outMargin),
                (self.center, self.center),
                (self.margin, self.outMargin), (self.outMargin, self.margin)  # 5
            ],
            [
                (self.margin, self.margin), (self.outMargin, self.outMargin),
                (self.margin, self.outMargin), (self.outMargin, self.margin),
                (self.center, self.margin), (self.center, self.outMargin)  # 6
            ]
        ]

    def draw(self, surface):
        pygame.draw.rect(surface, self.backgroundColor, pygame.Rect(
            self.position[0], self.position[1], self.size, self.size))
        pygame.draw.rect(surface, self.borderColor, pygame.Rect(
            self.position[0], self.position[1], self.size, self.size), self.borderThickness)
        for dot in self.dotPosition[self.diceValue - 1]:
            pygame.draw.circle(surface, self.dotColor, (
                self.position[0] + dot[0],
                self.position[1] + dot[1]),
                self.dotSize)


class DiceRoll:
    def __init__(self, diceRoll, size, position, gap, surface):
        self.diceDraw = []
        self.diceRoll = diceRoll
        self.size = size
        self.position = position
        self.gap = gap
        self.surface = surface
        for n in range(0, len(diceRoll)):
            self.diceDraw.append(
                Dice(diceRoll[n], size, (position[0] + n * (size + gap), position[1])))

    def __updateThrowAnimation(self):
        for n in range(0, len(self.diceRoll)):
            dice = Dice(random.randint(1, 6), self.size,
                        (self.position[0] + n * (self.size + self.gap), self.position[1]))
            dice.draw(self.surface)

    def draw(self, throwTime=0):
        # throwTime in seconds
        if(throwTime == 0):
            # no throw animation
            for dice in self.diceDraw:
                dice.draw(self.surface)
        else:
            # throw animation
            t = Timer(throwTime, self.__updateThrowAnimation)
            t.start()


pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

# Create The Backgound
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 160, 0))
screen.blit(background, (0, 0))

random.seed()

done = False
while (not done):
    pygame.display.set_caption(" FPS : {:.4}".format(clock.get_fps()))
    event = pygame.event.poll()

    for n in range(1, 7):
        dice = Dice(n, 50, (n * 60, 10))
        dice.draw(screen)

    for n in range(1, 7):
        dice = Dice(n, 25, (n * 30, 100))
        dice.draw(screen)

    diceRoll = [1, 2, 3, 4, 5, 6]
    diceRollDraw = DiceRoll(diceRoll, 50, (10, 200), 20, screen)
    diceRollDraw.draw()

    diceRoll = [2, 2, 2, 5, 3]
    diceRollDraw = DiceRoll(diceRoll, 50, (10, 300), 20, screen)
    diceRollDraw.draw(10)

    if (event.type == pygame.QUIT):
        done = True
    if (event.type == pygame.KEYDOWN):
        if (event.key == pygame.K_ESCAPE):
            done = True

    pygame.display.flip()
    clock.tick(120)
