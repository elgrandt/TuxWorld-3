
import pygame

class playerManager:
    def __init__(self):
        self.__player   = None
        self.__moveUp   = False
        self.__moveDown = False
        self.__moveRight= False
        self.__moveLeft = False
        self.__action   = False

    def logic_update(self,EVENTS):
        keyboard = EVENTS.get_keyboard()

        self.__moveUp   = keyboard[pygame.K_UP]
        self.__moveDown = keyboard[pygame.K_DOWN]
        self.__moveRight= keyboard[pygame.K_RIGHT]
        self.__moveLeft = keyboard[pygame.K_LEFT]
        self.__action   = keyboard[pygame.K_SPACE]

    def moveUp(self):
        return self.__moveUp
    def moveDown(self):
        return self.__moveDown
    def moveRight(self):
        return self.__moveRight
    def moveLeft(self):
        return self.__moveLeft
    def action(self):
        return self.__action

    def graphic_update(self,SCREEN):
        pass