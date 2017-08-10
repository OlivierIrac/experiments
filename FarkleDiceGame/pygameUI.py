'''
Created on 8 august 2017

@author: irac1
'''

import pygame
import random
from threading import Timer


class UIObject:
    def __init__(self, size, position, surface):
        self.size = size
        self.position = position
        self.surface = surface

    def isMouseInside(self):
        mx, my = pygame.mouse.get_pos()
        rect = (self.position[0], self.position[1], self.size, self.size)
        if (rect[0] <= mx <= rect[0] + rect[2] and rect[1] <= my <= rect[1] + rect[3]):
            return True
        else:
            return False

    def draw(self):
        raise NotImplementedError()  # pure virtual

    def handleEvent(self, event):
        raise NotImplementedError()  # pure virtual


class DiceUI(UIObject):
    def __init__(self, diceValue, size, position, surface):
        super().__init__(size, position, surface)
        self.diceValue = diceValue
        self.backgroundColor = (255, 255, 255)
        self.backgroundHoverColor = (190, 190, 255)
        self.backgroundSelectedColor = (150, 150, 255)
        self.borderColor = (0, 0, 0)
        self.borderSelectedColor = (0, 0, 0)
        self.dotColor = (0, 0, 0)
        self.selected = False
        self.borderThickness = 1
        self.borderSelectedThickness = 2
        self.dotSize = int(self.size / 10)
        self.topLeftMargin = int(self.size / 4)
        self.center = int(self.size / 2)
        self.bottomRightMargin = self.size - self.topLeftMargin
        self.dotPosition = [
            [
                (self.center, self.center)  # 1
            ],
            [
                (self.topLeftMargin, self.topLeftMargin), (self.bottomRightMargin, self.bottomRightMargin)  # 2
            ],
            [
                (self.topLeftMargin, self.topLeftMargin), (self.center, self.center),
                (self.bottomRightMargin, self.bottomRightMargin)  # 3
            ],
            [
                (self.topLeftMargin, self.topLeftMargin), (self.bottomRightMargin, self.bottomRightMargin),
                (self.topLeftMargin, self.bottomRightMargin), (self.bottomRightMargin, self.topLeftMargin)  # 4
            ],
            [
                (self.topLeftMargin, self.topLeftMargin), (self.bottomRightMargin, self.bottomRightMargin),
                (self.center, self.center),
                (self.topLeftMargin, self.bottomRightMargin), (self.bottomRightMargin, self.topLeftMargin)  # 5
            ],
            [
                (self.topLeftMargin, self.topLeftMargin), (self.bottomRightMargin, self.bottomRightMargin),
                (self.topLeftMargin, self.bottomRightMargin), (self.bottomRightMargin, self.topLeftMargin),
                (self.center, self.topLeftMargin), (self.center, self.bottomRightMargin)  # 6
            ]
        ]

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def toggleSelect(self):
        self.selected = not self.selected

    def handleEvent(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if (self.isMouseInside()):
                self.toggleSelect()

    def draw(self):
        rect = (self.position[0], self.position[1], self.size, self.size)
        if (self.isMouseInside()):
            pygame.draw.rect(self.surface, self.backgroundHoverColor, pygame.Rect(rect))
        elif (self.selected):
            pygame.draw.rect(self.surface, self.backgroundSelectedColor, pygame.Rect(rect))
        else:
            pygame.draw.rect(self.surface, self.backgroundColor, pygame.Rect(rect))
        if (self.selected):
            pygame.draw.rect(self.surface, self.borderSelectedColor,
                             pygame.Rect(rect), self.borderSelectedThickness)
        else:
            pygame.draw.rect(self.surface, self.borderColor,
                             pygame.Rect(rect), self.borderThickness)
        for dot in self.dotPosition[self.diceValue - 1]:
            pygame.draw.circle(self.surface, self.dotColor, (
                self.position[0] + dot[0],
                self.position[1] + dot[1]),
                self.dotSize)


class DiceRollUI(UIObject):
    def __init__(self, diceRoll, size, position, gap, surface):
        super().__init__(size, position, surface)
        self.diceDraw = []
        self.diceRoll = diceRoll
        self.gap = gap
        for n in range(0, len(diceRoll)):
            self.diceDraw.append(
                DiceUI(diceRoll[n], size, (position[0] + n * (size + gap), position[1]), surface))

    def __updateThrowAnimation(self):
        for n in range(0, len(self.diceRoll)):
            dice = DiceUI(random.randint(1, 6), self.size,
                          (self.position[0] + n * (self.size + self.gap), self.position[1]), self.surface)
            dice.draw(self.surface)

    def draw(self, throwTime=0):
        # throwTime in seconds
        if(throwTime == 0):
            # no throw animation
            for dice in self.diceDraw:
                dice.draw()
        else:
            # throw animation
            # FIXME: RuntimeError: can't start new thread
            t = Timer(throwTime, self.__updateThrowAnimation)
            t.start()

    def handleEvent(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            for dice in self.diceDraw:
                if (dice.isMouseInside()):
                    dice.toggleSelect()


pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

# Create The Backgound
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 160, 0))

random.seed()
UIObjects = []

for n in range(1, 7):
    dice = DiceUI(n, 50, (n * 60, 10), screen)
    UIObjects.append(dice)

for n in range(1, 7):
    dice = DiceUI(n, 25, (n * 30, 100), screen)
    UIObjects.append(dice)

diceRoll = [1, 2, 3, 4, 5, 6]
diceRollDraw = DiceRollUI(diceRoll, 50, (10, 200), 20, screen)
UIObjects.append(diceRollDraw)

diceRoll = [2, 2, 2, 5, 3]
diceRollDraw = DiceRollUI(diceRoll, 50, (10, 300), 20, screen)
UIObjects.append(diceRollDraw)

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
        UIObject.handleEvent(event)
        UIObject.draw()

    pygame.display.flip()
    clock.tick(120)
