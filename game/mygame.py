__author__ = 'ariel'

#Edicion 1
#aqui se haya el encargado de manegar los niveles, (por ejemplo la camara, check point, cambio de nivel, etc)

import elements
import random
import pygame
class ListElement:
    def __init__             (self          ):
        self.__ELEMENT = elements.element.Element()
        self.__NAME = ""
        self.__ID   = 0

    ### SET FUNCTIONS      ###
    def SetElement           (self,element  ):
        element.setListElementReference(self)
        self.__ELEMENT = element
    def SetName              (self,name     ):
        self.__NAME = name
    def SetId                (self,ID       ):
        self.__ID = ID
    def SetObjectsReference  (self,REFERENCE):
        self.__ELEMENT.setObjectsReference(REFERENCE)
    def SetCam               (self,CAM      ):
        self.__ELEMENT.SetCamera(CAM)

    ### GET FUNCTIONS      ###
    def GetName              (self          ):
        return self.__NAME
    def GetElement           (self          ):
        return self.__ELEMENT
    def GetId                (self          ):
        return self.__ID

    ### COMPARE FUNCTIONS  ###
    def isId(self,ID):
        if (self.GetId() == ID):
            return True
        return False

    ### UPDATING FUNCTIONS ###
    def logic_update         (self,EVENTS   ):
        self.__ELEMENT.logic_update(EVENTS)
    def graphic_update       (self,SCREEN   ):
        self.__ELEMENT.graphic_update(SCREEN)

class Phi:
    def __init__(self):
        self.__CAM = {"x":0,"y":0}
        self.__Index = 0
        self.__elements = []
        self.__focused = False
        self.__Energy = 4
        self.__Lifes = 3
        self.__Killed = False
    ### PARTICULAR FUNCIONS FOR USE ###

    def addElement(self,element,name):
        self.__Index += 1

        new_element = ListElement()
        new_element.SetElement(element)
        new_element.SetName(name)
        new_element.SetId(self.__Index)
        new_element.SetCam(self.__CAM)
        new_element.SetObjectsReference(self)

        self.__elements.append(new_element)

    ### UPDATING FUNCTIONS ###
    def logic_update             (self,EVENTS):
        for x in range(len(self.__elements)):
            listelement = self.__elements[x]

            listelement.logic_update(EVENTS)
        if (self.__focused):
            self.cameraUpdate()
    def graphic_update           (self,SCREEN):
        for x in range(len(self.__elements)):
            listelement = self.__elements[x]

            listelement.graphic_update(SCREEN)

    ### INDEX FUNCTIONS    ### Direct means no ListElement object ###
    def getElementIndexByName    (self,name        ):
        for x in range(len(self.__elements)):
            if (self.__elements[x].GetName() == name):
                return x
    def getElementReferenceByName(self,name        ):
        return self.__elements[ self.getElementIndexByName(name) ]

    def getElementsOfTag         (self,TAG,noIndex ):
        elements = []
        for x in range(len(self.__elements)):
            current = self.__elements[x]
            if (current.GetElement().isTag(TAG) and not current.isId(noIndex)):
                elements.append(current)

        return elements
    def getElementsOfTagDirect   (self,TAG,noIndex ):
        elements = []
        for x in range(len(self.__elements)):
            current = self.__elements[x]
            if (current.GetElement().isTag(TAG) and not current.isId(noIndex)):
                elements.append(current.GetElement())

        return elements

    def getAllElements           (self,noIndex     ):
        elements = []
        for x in range(len(self.__elements)):
            if (not self.__elements[x].isId(noIndex)):
                elements.append(self.__elements[x])
        return elements
    def getAllElementsDirect     (self,noIndex     ):
        elements = []
        for x in range(len(self.__elements)):
            if (not self.__elements[x].isId(noIndex)):
                elements.append(self.__elements[x].GetElement())
        return elements

    def getElementsOfType        (self,TYPE,noIndex):
        elements = []
        for x in range(len(self.__elements)):
            if (self.__elements[x].GetElement().isType(TYPE) and not self.__elements[x].isId(noIndex)):
                elements.append(self.__elements[x])

        return elements
    def getElementsOfTypeDirect  (self,TYPE,noIndex):
        elements = []
        for x in range(len(self.__elements)):
            if (self.__elements[x].GetElement().isType(TYPE) and not self.__elements[x].isId(noIndex)):
                elements.append(self.__elements[x].GetElement())

        return elements


    ### CAMERA ###
    def setCameraFocus(self,element):
        self.__focused = True
        self.__element = element
    def cameraUpdate  (self        ):
        STAGE_WIDTH, STAGE_HEIGHT = pygame.display.get_surface().get_size()
        if (self.__element.getNetaXPosition() > STAGE_WIDTH/8.0*5.0):
            Diference = self.__element.getNetaXPosition() - STAGE_WIDTH/8.0*5.0
            self.__CAM["x"] += Diference
        if (self.__element.getNetaXPosition() < STAGE_WIDTH/8.0*3.0):
            Diference = STAGE_WIDTH/8.0*3.0 - self.__element.getNetaXPosition()
            self.__CAM["x"] -= Diference
        if (self.__element.getNetaYPosition() > STAGE_HEIGHT/8.0*5.0):
            Diference = self.__element.getNetaYPosition() - STAGE_HEIGHT/8.0*5.0
            self.__CAM["y"] += Diference
        if (self.__element.getNetaYPosition() < STAGE_HEIGHT/8.0*3.0):
            Diference = STAGE_HEIGHT/8.0*3.0 - self.__element.getNetaYPosition()
            self.__CAM["y"] -= Diference

    ### GAME THINGS ###
    def RemoveEnergy(self,Force):
        for q in range(Force):
            self.__Energy -= 1
            if self.__Energy <= 0:
                self.__Lifes -= 1
                self.__Energy = 4
        if self.__Lifes <= 0:
            self.__Killed = True

class test_level:
    def __init__(self):
        self.phi = Phi()

        Background = elements.backgound.ClassicBackground.ClassicBackground(40,40,18,16,(0,111,255),0)
        self.phi.addElement(Background, "Background")

        WallA = elements.wall.ClassicWall(0,0,10,elements.wall.directions.HORIZONTAL)
        WallB = elements.wall.ClassicWall(0,840,10,elements.wall.directions.HORIZONTAL)
        WallC = elements.wall.ClassicWall(0,40,8,elements.wall.directions.VERTICAL)
        '''WallD = elements.wall.ClassicWall(920,40,8,elements.wall.directions.VERTICAL)'''
        Player= elements.TuxPlayer.player.TuxPlayer()
        Player.SetPosition((500,500))
        self.Manager= elements.TuxPlayer.manager.playerManager()
        Player.setPlayerManager(self.Manager)
        self.phi.addElement(WallA,"Wall A")
        self.phi.addElement(WallB,"Wall B")
        self.phi.addElement(WallC,"Wall C")
        '''self.phi.addElement(WallD,"Wall D")'''

        enemy = elements.enemy.InteligentClassicEnemy.InteligentClassicEnemy(100,100,2)
        self.phi.addElement(enemy,"Enemy")
        self.phi.addElement(Player,"Player")
        self.phi.setCameraFocus(Player)

    def logic_update  (self,EVENTS):
        self.phi.logic_update(EVENTS)
        self.Manager.logic_update(EVENTS)
    def graphic_update(self,SCREEN):
        self.phi.graphic_update(SCREEN)