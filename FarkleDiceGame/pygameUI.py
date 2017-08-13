'''
Created on 8 august 2017

@author: irac1
'''

import pygame
import random
from threading import Timer


def blit_text(surface, text, pos, font, color=(0, 0, 0)):
    # 2D array where each row is a list of words.
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    max_width = surface.get_width()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


class UIObject:
    def __init__(self, width, height, position, surface):
        self.width = width
        self.height = height
        self.position = position
        self.surface = surface

    def isMouseInside(self):
        mx, my = pygame.mouse.get_pos()
        rect = (self.position[0], self.position[1], self.width, self.height)
        if (rect[0] <= mx <= rect[0] + rect[2] and rect[1] <= my <= rect[1] + rect[3]):
            return True
        else:
            return False

    def draw(self):
        raise NotImplementedError()  # pure virtual

    def handleEvent(self, event):
        raise NotImplementedError()  # pure virtual


class ButtonUI(UIObject):
    def __init__(self, text, color, width, height, position, surface):
        self.heightMargin = 10
        self.widthMargin = 10
        if(height == 0):
            self.font = pygame.font.SysFont('Calibri', 10)
        else:
            self.font = pygame.font.SysFont('Calibri', height)
        self.height = self.font.size(text)[1] + self.heightMargin
        if(width == 0):
            self.width = self.font.size(text)[0] + self.widthMargin
        self.position = position
        self.surface = surface
        self.text = text
        self.textColor = pygame.Color('white')
        self.backgroundColor = color
        self.backgroundHoverColor = color
        self.borderColor = (0, 0, 0)
        self.borderHoverColor = (100, 100, 255)
        self.borderThickness = 1

    def handleEvent(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if (self.isMouseInside()):
                return "buttonClicked"

    def draw(self):
        rect = (self.position[0], self.position[1], self.width, self.height)
        if (self.isMouseInside()):
            pygame.draw.rect(self.surface, self.backgroundHoverColor, pygame.Rect(rect))
            pygame.draw.rect(self.surface, self.borderHoverColor,
                             pygame.Rect(rect), self.borderThickness)
        else:
            pygame.draw.rect(self.surface, self.backgroundColor, pygame.Rect(rect))
            pygame.draw.rect(self.surface, self.borderColor,
                             pygame.Rect(rect), self.borderThickness)

        blit_text(self.surface, self.text, (self.position[0] + int(
            self.widthMargin / 2), self.position[1] + int(self.heightMargin / 2)), self.font, self.textColor)


class DiceUI(UIObject):
    def __init__(self, diceValue, size, position, surface, selectable=True):
        super().__init__(size, size, position, surface)
        self.size = size
        self.diceValue = diceValue
        self.selectable = selectable
        self.backgroundColor = (255, 255, 255)
        self.backgroundHoverColor = (190, 190, 255)
        self.backgroundSelectedColor = (255, 255, 255)
        self.borderColor = (0, 0, 0)
        self.borderSelectedColor = (50, 50, 255)
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
        if(self.selectable):
            self.selected = True

    def unselect(self):
        self.selected = False

    def toggleSelect(self):
        if(self.selectable):
            self.selected = not self.selected

    def isSelected(self):
        return self.selected

    def handleEvent(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if (self.isMouseInside() and self.selectable):
                self.toggleSelect()

    def draw(self):
        rect = (self.position[0], self.position[1], self.size, self.size)
        if (self.isMouseInside() and self.selectable):
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
            if (self.dotSize >= 2):
                pygame.draw.circle(self.surface, self.dotColor, (
                    self.position[0] + dot[0],
                    self.position[1] + dot[1]),
                    self.dotSize)
            else:
                self.surface.fill(self.dotColor, (
                    (self.position[0] + dot[0] - 1,
                     self.position[1] + dot[1] - 1),
                    (2, 2)))


class DiceRollUI(UIObject):
    def __init__(self, diceRoll, gap, size, position, surface, selectable=True):
        super().__init__(len(diceRoll) * (size + gap), size, position, surface)
        self.size = size
        self.diceDraw = []
        self.diceRoll = diceRoll
        self.gap = gap
        self.selectable = selectable
        for n in range(0, len(diceRoll)):
            self.diceDraw.append(
                DiceUI(diceRoll[n], size, (position[0] + n * (size + gap), position[1]), surface, self.selectable))

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
                if(dice.isMouseInside()):
                    dice.toggleSelect()

    def getDiceSelection(self):
        diceSelection = []
        for dice in self.diceDraw:
            if(dice.isSelected()):
                diceSelection.append(dice.diceValue)
        return diceSelection
