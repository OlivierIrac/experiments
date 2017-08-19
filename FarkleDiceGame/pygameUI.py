'''
Created on 8 august 2017

@author: irac1
'''

import pygame
import random
from threading import Timer

font = ('Calibri', int(11 * 96 / 72))  # size in pixels = points * 96 / 72


def highlight(color):
    return tuple(min(c + 50, 255) for c in color)


def darken(color):
    return tuple(max(c - 50, 0) for c in color)


def blit_text(surface, text, pos, font, color=(0, 0, 0)):
    # 2D array where each row is a list of words.
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    max_width = surface.get_width()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
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
        self.isShown = True

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

    def show(self):
        self.isShown = True

    def hide(self):
        self.isShown = False


class ButtonUI(UIObject):
    def __init__(self, text, textColor, color, width, height, position, surface):
        super().__init__(width, height, position, surface)
        self.heightMargin = 10
        self.widthMargin = 10
        if(height == 0):
            self.font = pygame.font.SysFont(font[0], font[1], True)
        else:
            self.font = pygame.font.SysFont(font[0], height, True)
        self.height = self.font.size(text)[1] + 2 * self.heightMargin
        if(width == 0):
            self.width = self.font.size(text)[0] + 2 * self.widthMargin
        self.text = text
        self.textColor = textColor
        self.backgroundColor = color
        self.backgroundHoverColor = highlight(color)
        self.borderColor = darken(color)
        self.borderHoverColor = highlight(self.borderColor)
        self.borderThickness = 1

    def handleEvent(self, event):
        if(self.isShown and event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if (self.isMouseInside()):
                return "buttonPressed"

    def draw(self):
        if(self.isShown):
            rect = (self.position[0], self.position[1], self.width, self.height)
            if (self.isMouseInside()):
                pygame.draw.rect(self.surface, self.backgroundHoverColor, pygame.Rect(rect))
                pygame.draw.rect(self.surface, self.borderHoverColor,
                                 pygame.Rect(rect), self.borderThickness)
            else:
                pygame.draw.rect(self.surface, self.backgroundColor, pygame.Rect(rect))
                pygame.draw.rect(self.surface, self.borderColor,
                                 pygame.Rect(rect), self.borderThickness)

            blit_text(self.surface, self.text, (self.position[0] + self.widthMargin,
                                                self.position[1] + self.heightMargin), self.font, self.textColor)

    def update(self, text):
        self.text = text


class MsgBoxUI(UIObject):
    def __init__(self, text, textColor, color, width, height, fontSize, position, surface):
        super().__init__(width, height, position, surface)
        self.font = pygame.font.SysFont(font[0], font[1])
        self.leftMargin = 10
        self.topMargin = 10
        self.text = text
        self.textColor = textColor
        self.backgroundColor = color
        self.backgroundHoverColor = color
        self.borderColor = darken(color)
        self.borderHoverColor = highlight(self.borderColor)
        self.borderThickness = 1

    def handleEvent(self, event):
        pass

    def draw(self):
        rect = (self.position[0], self.position[1], self.width, self.height)
        if (self.isMouseInside()):
            pygame.draw.rect(
                self.surface, self.backgroundHoverColor, pygame.Rect(rect))
            pygame.draw.rect(self.surface, self.borderHoverColor,
                             pygame.Rect(rect), self.borderThickness)
        else:
            pygame.draw.rect(self.surface, self.backgroundColor, pygame.Rect(rect))
            pygame.draw.rect(self.surface, self.borderColor,
                             pygame.Rect(rect), self.borderThickness)

        blit_text(self.surface, self.text,
                  (self.position[0] + self.leftMargin, self.position[1] + self.topMargin), self.font, self.textColor)

    def update(self, text):
        self.text = text


class DiceUI(UIObject):
    def __init__(self, diceValue, size, position, surface, color=pygame.Color('white'), selectable=False):
        super().__init__(size, size, position, surface)
        self.size = size
        self.diceValue = diceValue
        self.selectable = selectable
        self.backgroundColor = color
        self.backgroundHoverColor = highlight(self.backgroundColor)
        self.backgroundSelectedColor = (255, 255, 255)
        self.borderColor = (100, 100, 100)
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

    def update(self, diceValue, color=pygame.Color('white'), selectable=False):
        self.backgroundColor = color
        self.diceValue = diceValue
        self.selectable = selectable

    def setColor(self, color=pygame.Color('white')):
        self.backgroundColor = color

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def toggleSelect(self):
        self.selected = not self.selected

    def isSelected(self):
        return self.selected

    def handleEvent(self, event):
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if (self.isMouseInside() and self.selectable):
                self.toggleSelect()

    def draw(self):
        if(self.diceValue == 0):
            return  # draw nothing "empty dice"
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
    def __init__(self, diceRoll, gap, size, position, surface, color=pygame.Color('white'), selectable=False, throwTime=0):
        super().__init__(len(diceRoll) * (size + gap), size, position, surface)
        self.size = size
        self.diceDraw = []
        self.diceRoll = diceRoll
        self.gap = gap
        self.selectable = selectable
        self.throwTime = throwTime
        self.animation = False
        self.animationEvent = pygame.USEREVENT
        self.nbDicesToDraw = len(diceRoll)
        self.color = color
        for n in range(0, len(diceRoll)):
            self.diceDraw.append(
                DiceUI(diceRoll[n], size, (position[0] + n * (size + gap), position[1]), surface, color, self.selectable))

    def update(self, diceRoll, color=pygame.Color('white'), selectable=False, throwTime=0):
        self.__init__(diceRoll, self.gap, self.size, self.position,
                      self.surface, self.color, selectable, throwTime)

    def startAnimation(self):
        if(len(self.diceRoll) != 0):
            self.animation = True
            pygame.time.set_timer(self.animationEvent, self.throwTime)
            self.nbDicesToDraw = 0
            return self.animationEvent

    def updateAnimation(self):
        if(self.animation):
            pygame.time.set_timer(self.animationEvent, self.throwTime)
            self.nbDicesToDraw += 1
            if(self.nbDicesToDraw == len(self.diceRoll)):
                self.stopAnimation()

    def stopAnimation(self):
        self.animation = False
        pygame.time.set_timer(self.animationEvent, 0)
        self.nbDicesToDraw = len(self.diceRoll)
        for dice in self.diceDraw:
            dice.setColor(self.color)

    def isAnimationComplete(self):
        return(not self.animation)

    def draw(self):
        if(self.nbDicesToDraw != 0):
            for n in range(0, self.nbDicesToDraw):
                self.diceDraw[n].draw()

    def handleEvent(self, event):
        for dice in self.diceDraw:
            dice.handleEvent(event)

    def getDiceSelection(self):
        diceSelection = []
        for dice in self.diceDraw:
            if(dice.isSelected()):
                diceSelection.append(dice.diceValue)
        return diceSelection
