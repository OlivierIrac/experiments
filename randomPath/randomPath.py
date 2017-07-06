'''
Created on 6 juil. 2017

@author: irac1
'''
import pygame
import random
import matplotlib.pyplot as plt



def drawRandomPath(surface,nbSteps):
    height=surface.get_height()
    width=surface.get_width()
    alphaSurface = pygame.Surface((width,height), pygame.SRCALPHA)
    y=int(height/2)
    yNormalized=nbSteps
    xStep=int(width/nbSteps)
    yStep=int(height/nbSteps)
    for x in range (0,width,xStep):
        direction=random.choice([-1,1])
        y2=y+yStep*direction
        yNormalized=yNormalized+direction
        pygame.draw.line(alphaSurface, (100,100,100),(x,y),(x+xStep,y2))
        y=y2
    surface.blit(alphaSurface,(0,0), None, pygame.BLEND_ADD)
    return yNormalized

pygame.init()
screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
random.seed()

done = False
i=0
nbSteps=50
repartition=[0]*nbSteps*2
while (not done):
    y=drawRandomPath(screen, nbSteps)
    repartition[y]+=1
    i+=1
    print(i)
    pygame.display.flip()



    event=pygame.event.poll()
    if (event.type == pygame.QUIT):
        done = True
    if (event.type == pygame.KEYDOWN):
        if (event.key == pygame.K_ESCAPE): 
            done = True

plt.plot(repartition)
plt.show()
