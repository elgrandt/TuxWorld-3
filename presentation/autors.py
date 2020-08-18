
#@Edicion 1
#Por: Ariel

#Se esta creando el efecto de aparicion de las letras de los creditos para el inicio del juego

import pygame
from load_data import fonts
from gui.Clasic import Clasic
import math
import random 

class Letter(Clasic):
    def __init__(self,letter,position):
        surface        = fonts.oliver(20).render(letter,1,(0,0,0))
        self.x,self.y  = position
        self.acelerate = True
        self.start     = False
        self.speed     = 0
        self           .UpdateSurface(surface)
        self.angle     = -30
        
    def logic_update(self,EVENTS):
        self.x += self.speed * math.sin(math.radians(self.angle))
        self.y += self.speed * math.cos(math.radians(self.angle))
    
    def graphic_update(self,SCREEN):
        SCREEN.blit(self.surface,(int(self.x),int(self.y)))
    
    def IncreaseSpeed(self):
        self.speed += 1
    
    def DecreaseSpeed(self):
        if (self.speed > 0):
            self.speed -= 1
class autorEffect:
    def __init__(self, text, position):
        self.letters     = []
        self.startMove   = False
        self.end         = False
        for x in range(len(text)):
            positionX = -400 * math.sin(math.radians(-30))
            positionY = -400 * math.cos(math.radians(-30))
            
            self.letters.append(Letter(text[x], (positionX+x*20+position[0],positionY+position[1])))
        
    def StartMove(self):
        self.letters[0].start = True
        
    def logic_update(self,EVENTS):
        for x in range(len(self.letters)):
            self.letters[x].logic_update(EVENTS)
            if (self.letters[x].start == True):
                if (self.letters[x].acelerate == True):
                    self.letters[x].IncreaseSpeed()
                    if (self.letters[x].speed > 1):
                        if (x != len(self.letters)-1):
                            self.letters[x+1].start = True
                        else:
                            self.end = True
                    if (self.letters[x].speed >= 20):
                        self.letters[x].acelerate = False
                        
                else:
                    self.letters[x].DecreaseSpeed()
                    
    def graphic_update(self,SCREEN):
        for x in range(len(self.letters)):
            self.letters[x].graphic_update(SCREEN)
    
    def End(self):
        return self.end
    
    def QuitLetters(self):
        for x in range(len(self.letters)):
            self.letters[x].speed = 60
            self.letters[x].angle = random.randrange(360)
            self.letters[x].acelerate = True
        
       
        