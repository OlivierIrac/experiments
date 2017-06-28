'''
Created on 15 juin 2017

@author: irac1
'''

import pygame
import os

class WindowManager:
    # Constants
    MIN_WINDOW_WIDTH=10
    MIN_WINDOW_HEIGHT=10
    WINDOW_DECORATION_COLOR=(0, 128, 255)
    ZOOM_SPEED=10
        
    def __init__ (self):
        self.windowsList=[]
        self.mxPress=0
        self.myPress=0
        self.windowSelected=False
        self.width0=0
        self.height0=0
        self.left0=0
        self.top0=0
        self.resize=False
        self.drag=False

    def add(self, windowHandler):
        self.windowsList.insert(0,windowHandler)
        
    def draw(self):
        screen.fill((0, 0, 0))
        for window in reversed(self.windowsList):
            window.draw()
            if (window.decoration):
                pygame.draw.rect(screen,WindowManager.WINDOW_DECORATION_COLOR,pygame.Rect(window.left,window.top,window.width,window.height),2)


    def selectWindow(self,window):
        (self.mxPress, self.myPress) = pygame.mouse.get_pos()             
        self.left0=window.left
        self.top0=window.top
        self.width0=window.width
        self.height0=window.height
        self.windowsList.remove(window)
        self.windowsList.insert(0,window)
        self.windowSelected=True
    
    def removeWindow(self,window):
        self.windowsList.remove(window)
        self.draw()
        
    def handleWindows(self,event):
        mx, my = pygame.mouse.get_pos()
        resizeCursor=False
        
        zoom=False
        for window in self.windowsList:
            if (window.isInBottomRightCorner(mx,my) or self.resize):  # click lower right corner = resize
                resizeCursor=True
            if (event.type == pygame.MOUSEBUTTONDOWN and not self.windowSelected):
                if (event.button == 1 and window.resize == False and window.drag == False):
                    if (window.isInBottomRightCorner(mx, my)): #click lower right corner = resize
                        self.selectWindow(window)
                        self.resize=True
                    if (window.left<=mx<window.left+window.width-2 and window.top<=my<window.top+window.height-2): #click inside shape = move
                        self.selectWindow(window)
                        self.drag=True
                        
                if (event.button == 3 and window.left<=mx<window.left+window.width and window.top<=my<window.top+window.height):
                    self.removeWindow(window)
                        
                if (window.left<=mx<window.left+window.width and window.top<=my<window.top+window.height and not zoom):
                    if (event.button == 4):
                        (window.width,window.height) = resizeProportional (window.width,window.height, window.width+2*WindowManager.ZOOM_SPEED,window.height+2*WindowManager.ZOOM_SPEED)
                        window.top-=WindowManager.ZOOM_SPEED
                        window.left-=WindowManager.ZOOM_SPEED
                        zoom=True
                    if (event.button == 5):
                        (window.width,window.height) = resizeProportional (window.width,window.height, window.width-2*WindowManager.ZOOM_SPEED,window.height-2*WindowManager.ZOOM_SPEED)
                        window.top+=WindowManager.ZOOM_SPEED
                        window.left+=WindowManager.ZOOM_SPEED
                        zoom=True

            if ((not pygame.mouse.get_pressed()[0]) and (not pygame.mouse.get_pressed()[2])):                    
                self.drag = False
                self.resize = False
                self.windowSelected=False
                    
            if (resizeCursor):  # click lower right corner = resize
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

            if (self.drag == True):
                self.windowsList[0].left = self.left0 + mx - self.mxPress
                self.windowsList[0].top = self.top0 + my - self.myPress
                
            if (self.resize == True):
                self.windowsList[0].width = self.width0 + mx - self.mxPress
                if (self.windowsList[0].width<=WindowManager.MIN_WINDOW_WIDTH):
                    self.windowsList[0].width=WindowManager.MIN_WINDOW_WIDTH
                self.windowsList[0].height = self.height0 + my - self.myPress    
                if (self.windowsList[0].height<=WindowManager.MIN_WINDOW_HEIGHT):
                    self.windowsList[0].height=WindowManager.MIN_WINDOW_HEIGHT
        self.draw()


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
    
class WindowHandler:
    def __init__(self, surface, left=0, top=0, width=800, height=600, decoration=False, proportional=False):
        self.left=left
        self.top=top
        self.width=width
        self.height=height
        self.oldWidth=self.width
        self.oldHeight=self.height
        self.surface=surface
        self.decoration=decoration
        self.proportional=proportional
        self.drag = False
        self.resize=False
        if (self.proportional):
            width=self.surface.get_width()
            height=self.surface.get_height()
            (width,height)=resizeProportional(width,height,self.width,self.height)
        else:
            width=self.width
            height=self.height                
        imgZoomed=pygame.transform.smoothscale(self.surface, (width, height))
        self.imgToBlit=imgZoomed.convert()


  
    def draw (self):
        if (self.width!=self.oldWidth or self.height!=self.oldHeight): #zoom only if size has changed
            self.oldWidth=self.width
            self.oldHeight=self.height
            if (self.proportional):
                width=self.surface.get_width()
                height=self.surface.get_height()
                (width,height)=resizeProportional(width,height,self.width,self.height)
            else:
                width=self.width
                height=self.height                
            imgZoomed=pygame.transform.smoothscale(self.surface, (width, height))
            self.imgToBlit=imgZoomed.convert()
        screen.blit(self.imgToBlit, (self.left, self.top))

    def isInBottomRightCorner (self,x,y):
        return ((self.left + self.width -2) <= x <= (self.left + self.width + 5) and (self.top + self.height -2) <= y <= (self.top + self.height + 5)) 
 
        
class ImageHandler(WindowHandler):   
    def __init__(self, file, left=0, top=0, width=800, height=600, decoration=False, proportional=False):
        WindowHandler.__init__(self,pygame.image.load(file),left, top, width, height, decoration, proportional)
        print ("Image %i %i",self.width, self.height)

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
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
        
class CountHandler(WindowHandler):
    def __init__(self, i0, left = 0, top = 0, width=800, height=600, decoration=False, proportional=False):
        surface=screen
        WindowHandler.__init__(self, surface, left, top, width, height, decoration, proportional)
        pygame.font.init() 
        self.i=i0
        
    def draw(self):
        font=pygame.font.SysFont('Calibri', self.height)
        self.i+=1
        s=""
        for j in range (self.i,self.i+10):
            s+=str(j)+"\n"
        blit_text(screen, s, (self.left, self.top), font, pygame.Color('white'))
    
windowManager=WindowManager()
img1Window=ImageHandler(os.path.join('data','2015_06_27_EOS 70D_0978.jpg'),50,50,100,100,True,True)
windowManager.add(img1Window)
img2Window=ImageHandler(os.path.join('data','alien1.jpg'),50,50,150,150)
windowManager.add(img2Window)
img3Window=ImageHandler(os.path.join('data','IMG_0760.jpg'),100,150,200,400)
windowManager.add(img3Window)
count1=CountHandler(0, 150, 150, 200, 50, True)
windowManager.add(count1)
count2=CountHandler(2000, 300, 150, 200, 50, True)
windowManager.add(count2)

done = False
while (not done):
    pygame.display.set_caption(" FPS : {:.4}".format(clock.get_fps()))    
    event=pygame.event.poll()
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
