
__author__ = 'ariel'
#Edicion 1
#Aqui esta una de las clases mas importantes, la clase del jugador Tux

import math
from game.elements.element import *

from load_data.images import tuxImages

import pygame

class TuxPlayer(Element):
    def __init__(self):
        self.start()
        self.setType("Player")
        self.setPhisicElement()
        self.__SPEED   =  5
        self.__ANGLE   =  5
        self.__WEAPONS = []
        self.__MODES   = []
        self.__MANAGER = None
        self.__STATUS  = "front"
        self.__state   = 0
        self.__toNext  = 0
        self.UpdateSurface(tuxImages["front"][0])

    ##### PRIVATE METHODS #####

    ##### CHECKING COLLISION ####
    def __checkUp    (self):
        return self.__checkSide(Collide.UP)
    def __checkDown  (self):
        return self.__checkSide(Collide.DOWN)
    def __checkLeft  (self):
        return self.__checkSide(Collide.LEFT)
    def __checkRight (self):
        return  self.__checkSide(Collide.RIGHT)
    def __checkSide(self,side):
        all_elements = self.getElementsOfTagDirect("Wall")
        for x in range(len(all_elements)):
            collide = self.getMaxCollide(all_elements[x])
            for y in range(len(collide)):
                if (collide[y]["COL"] == side):
                    return False
        return True

    def __move(self):
        self.SumX( math.sin(math.radians(self.__ANGLE)) * self.__SPEED)
        self.SumY( math.cos(math.radians(self.__ANGLE)) * self.__SPEED)
    def __unmove(self):
        self.SumX( math.sin(math.radians(self.__ANGLE)) * - self.__SPEED)
        self.SumY( math.cos(math.radians(self.__ANGLE)) * - self.__SPEED)
    def __unmoveX(self):
        self.SumX( math.sin(math.radians(self.__ANGLE)) * - self.__SPEED)
    def __unmoveY(self):
        self.SumY( math.cos(math.radians(self.__ANGLE)) * - self.__SPEED)

    def __updateMoving(self):
        UP    = self.__MANAGER.moveUp()
        DOWN  = self.__MANAGER.moveDown()
        LEFT  = self.__MANAGER.moveLeft()
        RIGHT = self.__MANAGER.moveRight()

        ### ANGLE WORKING ###

        moving = False
        if (UP and not DOWN):
            self.__STATUS = "back"
            moving = True
            angle = 180
            if (LEFT and not RIGHT):
                angle -= 45
            if (RIGHT and not LEFT):
                angle += 45
        if (DOWN and not UP):
            self.__STATUS = "front"
            moving = True
            angle = 0
            if (LEFT and not RIGHT):
                angle += 45
            if (RIGHT and not LEFT):
                angle -= 45
        if (LEFT and not RIGHT):
            self.__STATUS = "left-walk"
            moving = True
            angle = 270
            if (UP and not DOWN):
                angle -= 45
            if (DOWN and not UP):
                angle += 45
        if (RIGHT and not LEFT):
            self.__STATUS = "walk"
            moving = True
            angle = 90
            if (UP and not DOWN):
                angle += 45
            if (DOWN and not UP):
                angle -= 45

        if (moving):
            self.__ANGLE = angle

            ### MOVING WORKING ###
            self.__move()

            if (UP and not self.__checkUp()):
                self.__unmoveY()
            if (DOWN and not self.__checkDown()):
                self.__unmoveY()
            if (LEFT and not self.__checkLeft()):
                self.__unmoveX()
            if (RIGHT and not self.__checkRight()):
                self.__unmoveX()

            self.__updateImage()
    def __updateImage(self):
        if (self.__toNext == 5):
            self.__state += 1
            self.__toNext = 0
            self.__updateSurface()
        self.__toNext += 1
    def __updateSurface(self):
        if (self.__state >= len(tuxImages[self.__STATUS])):
            self.__state = 0
        self.UpdateSurface(tuxImages[self.__STATUS][self.__state])
    ##### PUBLIC METHODS #####
    def setPlayerManager(self,manager):
        """
        @type manager: Phi
        """
        self.__MANAGER = manager

    ## LOGIC AND GRAPHIC ##
    def plu             (self,EVENTS):

        self.__updateMoving()
    def pgu             (self,SCREEN):
        pass



