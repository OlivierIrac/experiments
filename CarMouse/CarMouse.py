'''
Created on 20 juin 2017

@author: irac1
'''
"""
Change the mouse cursor to a car using pygame.
With the help of: http://programarcadegames.com/index.php?lang=en Chapter 11. Controllers and Graphics.
By niquefaDiego
"""

import pygame

BLACK       = (   0,   0,   0 )
WHITE       = ( 255, 255, 255 )
RED         = ( 255,   0,   0 )
RED_220     = ( 220,   0,   0 ) #darker
RED_200     = ( 200,   0,   0 ) #even darker
SKY         = ( 223, 245, 243 )
GREY        = ( 200, 200, 200 )

size = (500,300)
pygame.init()
screen = pygame.display.set_mode ( size )
pygame.mouse.set_visible ( False ) #makes mouse invisible

#draw a car in position (x,y)
def draw_car ( x, y ):

    #draw basic car shape
    pol = []
    pol.append ( ( x-20, y ) )
    pol.append ( ( x-2, y ) )
    pol.append ( ( x-2, y-10 ) )
    pol.append ( ( x+7, y-10 ) )
    pol.append ( ( x+12, y-3 ) )
    pol.append ( ( x+20, y+2 ) )
    pol.append ( ( x+20, y+10 ) )
    pol.append     ( ( x-20, y+10 ) )
    pygame.draw.polygon ( screen, RED, pol )
    
    #degrade red
    pygame.draw.rect ( screen, RED_220, [x-20,y+4,40,3] )
    pygame.draw.rect ( screen, RED_200, [x-20,y+7,40,3] )
    
    #add window
    pol = []
    pol.append ( ( x, y-2 ) )
    pol.append ( ( x, y-8 ) )
    pol.append ( ( x+6, y-8 ) )
    pol.append ( ( x+10, y-2 ) )
    pygame.draw.polygon ( screen, SKY, pol )

    #add wheels
    pygame.draw.circle ( screen, BLACK, (x-10,y+10), 5 );
    pygame.draw.circle ( screen, BLACK, (x+10,y+10), 5 );
    pygame.draw.circle ( screen, GREY, (x-10,y+10), 2 );
    pygame.draw.circle ( screen, GREY, (x+10,y+10), 2 );

endProgram = False
while True:
    
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endProgram = True

    if endProgram:
        break

    #draw car
    screen.fill(WHITE) #clear screen
    pos = pygame.mouse.get_pos() #get mouse position
    draw_car ( pos[0], pos[1] ) #draw a car in mouse position
    pygame.display.flip() #update screen

pygame.quit()