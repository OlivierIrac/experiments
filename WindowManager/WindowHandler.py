'''
Created on 28 juin 2017

@author: irac1
'''
import pygame

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