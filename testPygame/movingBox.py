'''
Created on 15 juin 2017

@author: irac1
'''

import pygame
import os

# ajout comment


class Color:
    def __init__ (self,name,r,g,b):
        self.color=(r,g,b)
        self.name=name
        
colorDictionary={'blue':(0, 128, 255), 'orange':(255, 100, 0), 'white':(255,255,255)}

colorIdx='orange'

def resizeProportional (x1,y1,x2,y2):
    xRatio = float(x2)/float(x1)
    yRatio = float(y2)/float(y1)
    if (xRatio > yRatio): 
        x1=yRatio*x1
        y1=y2
    else:
        x1=x2
        y1=xRatio*y1
    return (int(x1),int(y1))



class MyWindow: 
    windowsList=[]
    zoomSpeed=10
    mxPress=0
    myPress=0
    
    @staticmethod
    def draw():
        screen.fill((0, 0, 0))
        for window in reversed(MyWindow.windowsList):
            window.drawFunction(window.x0,window.y0,window.width,window.height)
        
    def __init__ (self, drawFunction, xLeft = 0, yTop = 0, windowWidth=800, windowHeight=600):
        self.width=windowWidth
        self.height=windowHeight
        self.x0=xLeft
        self.y0=yTop
        self.drag = False
        self.resize=False
        self.drawFunction=drawFunction
        self.width0=self.width
        self.height0=self.height
        self.x00=self.x0
        self.y00=self.y0
        MyWindow.windowsList.insert(0,self)
#        MyWindow.windowsList.append(self)
        MyWindow.draw()
    
    def isInBottomRightCorner (self,x,y):
        return ((self.x0 + self.width -2) <= x <= (self.x0 + self.width + 5) and (self.y0 + self.height -2) <= y <= (self.y0 + self.height + 5)) 
 
    @staticmethod
    def handleWindows(event):
        mx, my = pygame.mouse.get_pos()
        resizeCursor=False
        windowSelected=False
        for window in MyWindow.windowsList:
            if (window.isInBottomRightCorner(mx,my) or window.resize):  # click lower right corner = resize
                resizeCursor=True
            if (event.type == pygame.MOUSEBUTTONDOWN and not windowSelected):
                if (event.button == 1 and window.resize == False and window.drag == False):
                    if (window.isInBottomRightCorner(mx, my)): #click lower right corner = resize
                        MyWindow.mxPress=mx
                        MyWindow.myPress=my               
                        #cursor = pygame.cursors.compile(pygame.cursors.sizer_xy_strings)
                        #colorIdx = 'white'
                        MyWindow.windowsList.remove(window)
                        MyWindow.windowsList.insert(0,window)
                        window.resize=True
                        window.width0=window.width
                        window.height0=window.height
                        windowSelected=True
                    if (window.x0<=mx<window.x0+window.width-2 and window.y0<=my<window.y0+window.height-2): #click inside shape = move
                        MyWindow.mxPress=mx
                        MyWindow.myPress=my               
                        window.drag=True
                        window.x00=window.x0
                        window.y00=window.y0
                        MyWindow.windowsList.remove(window)
                        MyWindow.windowsList.insert(0,window)
                        windowSelected=True

                if (event.button == 4):
                    (window.width,window.height) = resizeProportional (window.width,window.height, window.width+MyWindow.zoomSpeed,window.height+MyWindow.zoomSpeed)
                if (event.button == 5):
                    (window.width,window.height) = resizeProportional (window.width,window.height, window.width-MyWindow.zoomSpeed,window.height-MyWindow.zoomSpeed)

            if ((not pygame.mouse.get_pressed()[0]) and (not pygame.mouse.get_pressed()[2])):                    
                window.drag = False
                window.resize = False
                    
            if (resizeCursor):  # click lower right corner = resize
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

            if (window.drag == True):
                window.x0 = window.x00 + mx - MyWindow.mxPress
                window.y0 = window.y00 + my - MyWindow.myPress
                
            if (window.resize == True):
                window.width = window.width0 + mx - MyWindow.mxPress
                window.height = window.height0 + my - MyWindow.myPress    

        MyWindow.draw()


pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    
class imgHandle:
    def __init__(self, surface):
        self.w=0
        self.h=0
        self.surface=surface
        self.imgToBlit=surface.convert()
        
    def Draw (self,x0,y0,w,h):
        if (self.w!=w or self.h!=h):
            self.w=w
            self.h=h
            print ("zoom")
            imgZoomed=pygame.transform.smoothscale(self.surface, (self.w, self.h))
            self.imgToBlit=imgZoomed.convert()
        screen.blit(self.imgToBlit, (x0, y0))

img1=pygame.image.load(os.path.join('data','2015_06_27_EOS 70D_0978.jpg'))
img1Handle=imgHandle(img1)
img2=pygame.image.load(os.path.join('data','alien1.jpg'))
img2Handle=imgHandle(img2)         
img3=pygame.image.load(os.path.join('data','IMG_0760.jpg'))
img3Handle=imgHandle(img3)         

clock = pygame.time.Clock()
done = False

img1Window=MyWindow(img1Handle.Draw,0,0,100,100)
img2Window=MyWindow(img2Handle.Draw,50,50,150,150)
img3Window=MyWindow(img3Handle.Draw,100,150,200,400)

while (not done):
    pygame.display.set_caption(" FPS : {:.4}".format(clock.get_fps()))
    
    for event in pygame.event.get():
        MyWindow.handleWindows(event)

        if (event.type == pygame.QUIT):
            done = True
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_ESCAPE): 
                done = True
        if (event.type == pygame.VIDEORESIZE):
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
    pygame.display.flip()
    clock.tick(120)
