'''
Created on 28 juin 2017

@author: irac1
'''
import pygame
from utils import resizeProportional,blit_text
  
class WindowHandler:
    def __init__(self, surface, left=0, top=0, width=800, height=600, title="", decoration=True, proportional=False):
        self.left=left
        self.top=top
        self.width=width
        self.height=height
        self.oldWidth=self.width
        self.oldHeight=self.height
        self.surface=surface
        self.decoration=decoration
        self.decorationHandler=None
        self.proportional=proportional
        self.drag = False
        self.resize=False
        self.paused=False
        self.title=title
        if (self.proportional):
            width=self.surface.get_width()
            height=self.surface.get_height()
            (width,height)=resizeProportional(width,height,self.width,self.height)
        else:
            width=self.width
            height=self.height                
        imgZoomed=pygame.transform.smoothscale(self.surface, (width, height))
        self.imgToBlit=imgZoomed.convert()


  
    def draw (self, surface):
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
        surface.blit(self.imgToBlit, (self.left, self.top))

    def isInBottomRightCorner (self,x,y):
        return ((self.left + self.width -2) <= x <= (self.left + self.width + 5) and (self.top + self.height -2) <= y <= (self.top + self.height + 5)) 
    
    def pause(self):
        self.paused=True
    def unpause(self):
        self.paused=False
    def exit(self):
        print ("Bye")
        
        
 
        
class ImageHandler(WindowHandler):   
    def __init__(self, file, left=0, top=0, width=800, height=600, decoration=True, proportional=False):
        WindowHandler.__init__(self,pygame.image.load(file),left, top, width, height, file, decoration, proportional)
        
class CountHandler(WindowHandler):
    def __init__(self, i0, surface, left = 0, top = 0, width=800, height=600, decoration=True, proportional=False):
        WindowHandler.__init__(self, surface, left, top, width, height, "Count", decoration, proportional)
        pygame.font.init() 
        self.i=i0
        
    def draw(self,surface):
        font=pygame.font.SysFont('Calibri', self.height)
        if (not self.paused):
            self.i+=1
        s=""
        for j in range (self.i,self.i+10):
            s+=str(j)+"\n"
        blit_text(surface, s, (self.left, self.top), font, pygame.Color('white'))