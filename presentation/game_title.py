
from load_data.fonts import *
from gui.Clasic import Clasic
import random
import math
import pygame

NOSTART      = 0
ACELERATE    = 1
DESACELERATE = 2
UNROTATE     = 3
END          = 4
GOUP         = 5
WAIT         = 6
FINALEND     = 7

class Letter(Clasic):
    def __init__(self,letter,position):
        boldGraph     = ubuntu_bold_graph(70)
        surfaceLetter = boldGraph . render(letter,0,(0,0,0))
        self.angle    = -50
        self.speed    = 0
        self.status   = NOSTART
        self.rotation = -30
        self.lr       = 3456
        self.waiting  = 0
        
        self.x = position[0] - math.sin(math.radians(self.angle)) * 25 * 100 / 2
        self.y = position[1] - math.cos(math.radians(self.angle)) * 25 * 100 / 2

        self.goX = position[0]
        self.goY = position[1]

        self.UpdateSurface(surfaceLetter)
        self.actualSurface = surfaceLetter
        
    def graphic_update(self,SCREEN):
        SCREEN.blit(self.actualSurface,(self.x,self.y))

    def skip(self):
        self.status = FINALEND
        self.rotation = 0
        self.x = self.goX
        self.y = self.goY

    def logic_update(self,EVENTS):    

        if (self.rotation != self.lr):
            self.actualSurface = pygame.transform.rotate(self.surface,self.rotation)
            self.lr = self.rotation
            
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y += math.cos(math.radians(self.angle)) * self.speed
        if (self.status == ACELERATE):
            self.speed += 2
            if (self.speed >= 50):
                self.status = DESACELERATE
        elif (self.status == DESACELERATE):
            self.speed -= 2
            if (self.speed == 0):
                self.status = END
        elif (self.status == UNROTATE):
            if (self.rotation < 0):
                self.rotation += 3
            else:
                self.status  = WAIT
                self.waiting = 40 
        elif (self.status == WAIT):
            self.waiting -= 1
            if (self.waiting == 0):
                self.status = GOUP
        elif (self.status == GOUP):
            if (self.y > 50):
                self.y -= 5
            else:
                self.status = FINALEND

    def startAnimation(self):
        if (self.status == NOSTART):
            self.status = ACELERATE
    
        
    
class GameTitle:
    MESSAGE = "Tux World 3"
    LETTERS = []
    wait_rotate = 0
    status = "normal"
    def __init__(self):
        pass
    
    def set_position(self,position):
        self.LETTERS = []
        aumento = 0
        
        for x in range(len(self.MESSAGE)):
            hipotetica = ubuntu_bold_graph(70).render(self.MESSAGE[x],0,(0,0,0))
            
            letter = Letter(self.MESSAGE[x],(position[0] + aumento,position[1]))
            self.LETTERS.append(letter)
            
            aumento += hipotetica.get_size()[0]+10
        self.aumento = aumento
        self.H = hipotetica.get_size()[1]

    def skip(self):
        for x in range(len(self.LETTERS)):
            self.LETTERS[x].skip()
            self.LETTERS[x].y = 50

        self.status = "End"

    def logic_update(self,EVENTS):
        
        for x in range(len(self.LETTERS)):
            self.LETTERS[x].logic_update(EVENTS)
            if (self.LETTERS[x].speed > 2 and self.LETTERS[x].status == ACELERATE):
                if (x != len(self.LETTERS)-1):
                    self.LETTERS[x+1].startAnimation()
                else:
                    self.status = "Wait rotate"
                    self.wait_rotate = 40
                    
        if (self.status == "Wait rotate"):
            self.wait_rotate -= 1
            if (self.wait_rotate == 0):
                self.status = "Unrotate"
                self.unRotate()
       
        elif (self.status == "Unrotate"):
            if (self.LETTERS[0].status == FINALEND):
                self.status = "End"
        
        
    def graphic_update(self,SCREEN):
        for x in range(len(self.LETTERS)):
            self.LETTERS[x].graphic_update(SCREEN)
            
    def start(self):
        self.LETTERS[0].startAnimation()

    def unRotate(self):
        for x in range(len(self.LETTERS)):
            self.LETTERS[x].status = UNROTATE

            