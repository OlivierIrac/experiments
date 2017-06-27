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
    MIN_WINDOW_WIDTH=10
    MIN_WINDOW_HEIGHT=10
    windowsList=[]
    zoomSpeed=10
    mxPress=0
    myPress=0
    
    @staticmethod
    def draw():
        screen.fill((0, 0, 0))
        for window in reversed(MyWindow.windowsList):
            window.drawFunction(window.left,window.top,window.width,window.height)
            if (window.decoration):
                pygame.draw.rect(screen,colorDictionary['blue'],pygame.Rect(window.left,window.top,window.width,window.height),2)
                
        
    def __init__ (self, drawFunction, left = 0, top = 0, windowWidth=800, windowHeight=600, decoration=False):
        self.width=windowWidth
        self.height=windowHeight
        self.left=left
        self.top=top
        self.drag = False
        self.resize=False
        self.drawFunction=drawFunction
        self.width0=self.width
        self.height0=self.height
        self.left0=self.left
        self.top0=self.top
        self.decoration=decoration
        MyWindow.windowsList.insert(0,self)
#        MyWindow.windowsList.append(self)
        MyWindow.draw()
    
    def isInBottomRightCorner (self,x,y):
        return ((self.left + self.width -2) <= x <= (self.left + self.width + 5) and (self.top + self.height -2) <= y <= (self.top + self.height + 5)) 
 
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
                    if (window.left<=mx<window.left+window.width-2 and window.top<=my<window.top+window.height-2): #click inside shape = move
                        MyWindow.mxPress=mx
                        MyWindow.myPress=my               
                        window.drag=True
                        window.left0=window.left
                        window.top0=window.top
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
                window.left = window.left0 + mx - MyWindow.mxPress
                window.top = window.top0 + my - MyWindow.myPress
                
            if (window.resize == True):
                window.width = window.width0 + mx - MyWindow.mxPress
                if (window.width<=MyWindow.MIN_WINDOW_WIDTH):
                    window.width=MyWindow.MIN_WINDOW_WIDTH
                window.height = window.height0 + my - MyWindow.myPress    
                if (window.height<=MyWindow.MIN_WINDOW_HEIGHT):
                    window.height=MyWindow.MIN_WINDOW_HEIGHT
        MyWindow.draw()



    
class ImageHandle:
    def __init__(self, file, proportional=False):
        self.w=0
        self.h=0
        self.surface=pygame.image.load(file)
        self.imgToBlit=self.surface.convert()
        self.proportional=proportional
        
    def Draw (self,left,top,w,h,):
        if (self.w!=w or self.h!=h):
            self.w=w
            self.h=h
            if (self.proportional):
                width=self.surface.get_width()
                height=self.surface.get_height()
                (width,height)=resizeProportional(width,height,w,h)
            else:
                width=w
                height=h                
            imgZoomed=pygame.transform.smoothscale(self.surface, (width, height))
            self.imgToBlit=imgZoomed.convert()
        screen.blit(self.imgToBlit, (left, top))



pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

img1Window=MyWindow(ImageHandle(os.path.join('data','2015_06_27_EOS 70D_0978.jpg'),True).Draw,0,0,100,100,True)
img2Window=MyWindow(ImageHandle(os.path.join('data','alien1.jpg')).Draw,50,50,150,150)
img3Window=MyWindow(ImageHandle(os.path.join('data','IMG_0760.jpg')).Draw,100,150,200,400)

done = False
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
