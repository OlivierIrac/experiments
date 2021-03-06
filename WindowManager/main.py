'''
Created on 28 juin 2017

@author: irac1
'''
import pygame
import os
from WindowManager import *
from WindowHandler import * 

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()
windowManager = WindowManager(screen)

img1Window = ImageHandler(os.path.join('data', '2015_06_27_EOS 70D_0978.jpg'), 50, 50, 100, 100, True, True)
windowManager.add(img1Window)
img2Window = ImageHandler(os.path.join('data', 'alien1.jpg'), 50, 50, 150, 150, False)
windowManager.add(img2Window)
img3Window = ImageHandler(os.path.join('data', 'IMG_0760.jpg'), 100, 150, 200, 400, False)
windowManager.add(img3Window)
count1 = CountHandler(0, screen, 150, 150, 200, 50, True)
windowManager.add(count1)
count2 = CountHandler(2000, screen, 300, 150, 200, 50, True)
windowManager.add(count2)

done = False
while (not done):
    pygame.display.set_caption(" FPS : {:.4}".format(clock.get_fps()))
    event = pygame.event.poll()
    windowManager.handleWindows(event)

    if (event.type == pygame.QUIT):
        done = True
    if (event.type == pygame.KEYDOWN):
        if (event.key == pygame.K_ESCAPE):
            done = True
    if (event.type == pygame.VIDEORESIZE):
        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    pygame.display.flip()
    clock.tick(120)
