import math
import pygame
import random
import events
from random import randrange
from utils import background

#Edicion: 1
#Por: Ariel

#Sera el fondo de la presentacion y probablemente tambien del menu

class Point:
    x,y     = 0,0
    angle   = 0
    speed   = 5
    LOOPS   = 0
    STOPPER = 40
    def __init__(self,position,angle,speed):
        self.x,self.y = position
        self.angle    = angle
        self.speed    = speed
        
    def logic_update(self,EVENTS):
        if (self.LOOPS == 0):
            self.x += math.sin(math.radians(self.angle)) * self.speed
            self.y += math.cos(math.radians(self.angle)) * self.speed
            
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y += math.cos(math.radians(self.angle)) * self.speed
        
        if (self.LOOPS % self.STOPPER == 0 and self.speed > 1):
            self.speed += 1
            if (self.STOPPER > 1):
                self.STOPPER = self.STOPPER / 2
        
        self.LOOPS += 1
        
        
    def graphic_update(self,SCREEN):
        pygame.draw.circle(SCREEN,(255,255,255),(int(self.x),int(self.y)),1)
class Background:
    POINTS = []
    LOOPS  = 0
    PERIOD = 1
    __COLOR= background.cBackground()
    def __init__(self):
        
        self.__COLOR.set_min_blue(100)
        self.__COLOR.set_min_red(100)
        self.__COLOR.set_min_green(100)
        self.__COLOR.SetSpeed(3)
    
    def logic_update(self,EVENTS):
        self.__COLOR.update()
        
        for x in range(len(self.POINTS)):
            self.POINTS[x].logic_update(EVENTS)
        if (self.LOOPS % self.PERIOD == 0):
            for y in range(2):
                self.AddPoint()
        self.LOOPS += 1
        
    def graphic_update(self,SCREEN):
        SCREEN.fill(self.__COLOR.GetColor())
        
        for x in range(len(self.POINTS)):
            self.POINTS[x].graphic_update(SCREEN)
            
    def AddPoint(self):
        STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()
        point = Point((STAGE_WIDTH / 2, STAGE_HEIGHT / 2), random.randrange(360), 5)
        point.logic_update(events.events())
        self.POINTS.append(point)