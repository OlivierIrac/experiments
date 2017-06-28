'''
Created on 15 juin 2017

@author: irac1
'''

from WindowHandler import *

class WindowManager:
    # Constants
    MIN_WINDOW_WIDTH=10
    MIN_WINDOW_HEIGHT=10
    WINDOW_DECORATION_COLOR=(0, 128, 255)
    ZOOM_SPEED=10
        
    def __init__ (self, surface):
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
        self.surface=surface

    def add(self, windowHandler):
        self.windowsList.insert(0,windowHandler)
        
    def draw(self):
        #pause all but top window
        for windows in self.windowsList:
            windows.pause()
        if (len(self.windowsList)!=0):
            self.windowsList[0].unpause()
        self.surface.fill((0, 0, 0))
        for window in reversed(self.windowsList):
            window.draw(self.surface)
            if (window.decoration):
                pygame.draw.rect(self.surface,WindowManager.WINDOW_DECORATION_COLOR,pygame.Rect(window.left,window.top,window.width,window.height),2)


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
        window.exit()
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



    
