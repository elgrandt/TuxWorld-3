#Menu del juego

#@Edicion 1
#Por: Ariel
#Se creo el selection, se le dieron propiedades de titulo fondo y poscision
#Edicion 2
#Por: Dylan
#Cree las funciones para generar los distintos tipos de surface dependiendo de su el mouse esta encima o precionando
#Edicion 3
#Por: Ariel
#cambios para cursor
#Edicion 4
#Por: Dylan
#Agregue la opcion para que se pueda tener color degradado
#Edicion 5
#por: Dylan
#Hice lo basico de la clase menu que juntan todos los botones y agregue para que se puedan mover los botones con las flechas 
#Edicion 6
#por: Ariel
#Terminando el menu en su conjunto


import pygame
import Clasic
from gui import add_border
from load_data.fonts import *
from load_data.images import *
import Gradient
import MenuActions
import json
import math

PLACED    =  0
MOVING    =  1
BACKSIDE  = -1
FRONTSIDE =  1

#selection, una opcion del menu


class changeSize(Clasic.Clasic2):
    def __init__(self,TITLE,POSITION,ZOOM):
        self.__TITLE      = TITLE
        self.__ZOOM       = ZOOM
        self.__LZOOM      = ZOOM
        self.SetPosition(POSITION)
        self.__SELECTED   = False
        self.__FONT       = ubuntu_bold_graph(30)
        self.image        = None

        self.updateSurface()
        self.SetCursorChange()

    def graphic_update(self,SCREEN):
        SCREEN.blit(self.surface,(self.getPosition()))
    
    def logic_update(self,EVENTS):
        if (self.__ZOOM != self.__LZOOM):
            self         .   updateSurface()
            self.__LZOOM =   self.__ZOOM
        self.SetEvents(EVENTS)
        self.Focused()
    def updateSurface(self):
        surface       =   pygame.surface.Surface((300,100))
        surface       .  fill((247, 190, 129))
        
        add_border    .  add_border(surface, (0,0,0), 4, 4, 4, 4)
        
        RenderText    =  self.__FONT.render(self.__TITLE,0,(0,0,0))
        TW , TH       =  RenderText.get_size()
        
        textX         =  300/2 - TW / 2
        textY         =  100/2 - TH / 2
        
        surface       .  blit(RenderText,(textX,textY))

        if (self.image != None):
            TW , TH = self.image.get_size()

            imageX = 300/2 - TW / 2
            imageY = 100/2 - TH / 2

            surface.blit(self.image,(imageX,imageY))

        final_surface =  pygame.transform.scale(surface,(int(300*self.__ZOOM),int(100*self.__ZOOM)))
        
        self          .  UpdateSurface(final_surface)
    def SetZoom(self,zoom):
        self.__ZOOM   = zoom
    
    def setCam(self,camy):
        self.__CAMY = camy
        
    def goUp(self):
        self.SetY( self.GetY() + 5)
        
    def goDown(self):
        self.SetY( self.GetY() - 5)

    def CenteredImage(self,image):
        self.image = image

class MenuOption:
    def __init__(self,ACTION,PARAMETERS,TITLE,POSITION,ZOOM):
        self.__ACTION     = ACTION
        self.__PARAMETERS = PARAMETERS
        button            = changeSize(TITLE, POSITION, ZOOM)
        self.__BUTTON     = button

    def setButtonCenteredImage(self,image):
        self.__BUTTON.CenteredImage(image)

    def GetButton(self):
        return self.__BUTTON
    
    def GetAction(self):
        return self.__ACTION
    
    def GetParameters(self):
        return self.__PARAMETERS

    def GetX(self):
        return self.__BUTTON.get_position()[0]
    
    def GetY(self):
        return self.__BUTTON.getPosition()[1]
    
    def Pressed(self):
        return self.__BUTTON.Pressed()

    def SetX(self,x):
        self.__BUTTON.SetX(x)

    def SetY(self,y):
        self.__BUTTON.SetY(y)

class Menu2:
    def __init__(self,position):
        self.__SELECTED  = 0
        self.__STATUS    = MOVING
        self.__ACTION    = MenuActions.NOSET
        self.__PARAMS    = {}

        self.__x,self.__y = position
        self.__TOADD = []
        self.__options = []
        self.bloqued = False

    def block(self):
        self.bloqued = True

    def unblock(self):
        self.bloqued = False

    def AddOption(self,optionName,ACTION,PARAMETERS):
        self.__TOADD.append({"title":optionName,"action":ACTION,"parameters":PARAMETERS})

    def StartOptions(self):

        for x in range(len(self.__TOADD)):
            title = self.__TOADD[x]["title"]
            action= self.__TOADD[x]["action"]
            params= self.__TOADD[x]["parameters"]
            
            self.__options.append(MenuOption(action,params,title,(0,self.getStart()),0))
        self.__TOADD = []

    def addReturnButton(self,image,ACTION,PARAMETERS):
        option = MenuOption(ACTION,PARAMETERS,"",(0,self.getStart()),0)
        option.setButtonCenteredImage(image)
        self.__options.append(option)

    def getStart(self):
        if (len(self.__options) == 0):
            start = 0
        else:
            start = self.__options[len(self.__options)-1].GetY()+125
        return start
    def goUp(self):
        for x in range(len(self.__options)):
            self.__options[x].GetButton().goUp()
    
    def goDown(self):
        for x in range(len(self.__options)):
            self.__options[x].GetButton().goDown()
               
    def logic_update(self,EVENTS):

        MOUSEX,MOUSEY = EVENTS.get_mouse().get_position()
        RX,RY         = MOUSEX - self.__x , MOUSEY - self.__y
        
        if (self.__STATUS == PLACED and not self.bloqued):
            if (RY > 200):
                if (self.__SELECTED < len(self.__options)-1):
                    self.__SELECTED += 1
                    self.__STATUS = MOVING
            elif (RY < 100):
                if (self.__SELECTED > 0):
                    self.__SELECTED -= 1
                    self.__STATUS = MOVING

        elif (self.__STATUS == MOVING):
            if   (self.__options[self.__SELECTED].GetY() < 100):
                self.goUp  ()
            elif (self.__options[self.__SELECTED].GetY() > 100):
                self.goDown()
            else:
                self.__STATUS = PLACED
                
        for x in range(len(self.__options)):
            EVENTS.generate_relative((self.__x,self.__y))
            self  .__options[x].GetButton().logic_update(EVENTS)

            center_distance = abs(self.__options[x].GetY()-100)
            
            zoom = 1.0 / math.pow(2.0, (center_distance / 40.0))
            
            self.__options[x].GetButton().SetZoom(zoom)
            if (self.__options[x].Pressed() and not self.bloqued):
                self.__ACTION = self.__options[x].GetAction()
                self.__PARAMS = self.__options[x].GetParameters()

            EVENTS.delete_relative()

    def getCurrentAction(self):
        action = self.__ACTION
        params = self.__PARAMS
        self.__ACTION = MenuActions.NOSET
        self.__PARAMS = {}
        final = {"action":action,"params":params}
        
        return final
    
    def graphic_update(self,SCREEN):
        surface = pygame.surface.Surface((300,300),pygame.SRCALPHA,32)
        surface.convert_alpha()
        
        for x in range(len(self.__options)):
            self.__options[x].GetButton().graphic_update(surface)
        
        SCREEN.blit(surface,(self.__x,self.__y))
        
    def SetPosition(self,position):
        self.__x, self.__y = position
    
    def GetX(self):
        return self.__x
    
    def GetY(self):
        return self.__y
    
    def moveLeft(self):
        self.__x -= 10
        
    def moveRight(self):
        self.__x += 10