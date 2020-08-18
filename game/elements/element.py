#Edicion 1
#Aqui la clase de donde todos los objetos heredaran


### "CASI" TERMINADA ###


from load_data.images import error_elemento
from load_data.images.load import *
from gui import Clasic
import pygame
import math

class Collide:
    UP    = 0
    DOWN  = 1
    LEFT  = 2
    RIGHT = 3

class Element(Clasic.Clasic3):
    ### TO BEGIN ELEMENT STRUCTURE ###
    def start(self):

        self.__CAM = {"x":0,"y":0}
        self.UpdateSurface(error_elemento)

        self.__TAG     = []
        self.__TYPE    = "None"
        self.__visible = True

        self.__OBJECTS    = []
        self.__listObject = None
        self.__netaXposition = 0
        self.__netaYposition = 0

    ### SETTING A ELEMENT TO BE PHISIC ###
    def setPhisicElement(self):
        self.addTag("Phisical")
    def setInvisible    (self):
        self.__visible = False
    def setVisible      (self):
        self.__visible = True

    ### SETTING ELEMENT CAMERA ###
    def SetCamera(self,cam):
        self.__CAM = cam
    def GetCamera(self    ):
        return self.__CAM
    ### OUTSIDE INFO FUNCTIONS ###
    ### TAG AND TYPE FUNCTIONS ###
    def addTag    (self,TAG     ):
        self.__TAG.append(TAG)
    def setType   (self,type    ):
        self.__TYPE = type
    def deleteTag (self,TAG     ):
        for x in range(len(self.__TAG)):
            if (self.__TAG[x] == TAG):
                del self.__TAG[x]
                return True
        return False
    def isTag     (self,TAG     ):
        for x in range(len(self.__TAG)):
            if (self.__TAG[x] == TAG):
                return True
        return False
    def isType    (self,compTYPE):
        if (self.__TYPE == compTYPE):
            return True
        return False
    def getMyId   (self         ):
        return self.__listObject.GetId()

    ### SETTING ELEMENTS AND LIST ELEMENT REFERENCE ###
    def setObjectsReference    (self,REFERENCE):
        self.__OBJECTS = REFERENCE
    def getObjectsReference    (self          ):
        return self.__OBJECTS
    def setListElementReference(self,REFERENCE):
        self.__listObject = REFERENCE
    def getListElementReference(self          ):
        return self.__listObject

    ### ANOTHER ELEMENTS FUNCTIONS ###
    def RemoveEnergy(self,Force):
        self.getObjectsReference().RemoveEnergy(Force)

    def getElementsOfTag                (self,TAG ):
        return self.getObjectsReference().getElementsOfTag(TAG,self.getMyId())
    def getElementsOfTagDirect          (self,TAG ):
        return self.getObjectsReference().getElementsOfTagDirect(TAG,self.getMyId())

    def getElementsOfType               (self,TYPE):
        return self.getObjectsReference().getElementsOfType(TYPE,self.getMyId())
    def getElementsOfTypeDirect         (self,TYPE):
        return self.getObjectsReference().getElementsOfTypeDirect(TYPE,self.getMyId())

    def getAllElements                  (self     ):
        return self.getObjectsReference().getAllElements(self.getMyId())
    def getAllElementsDirect            (self     ):
        return self.getObjectsReference().getAllElementsDirect(self.getMyId())

    ### GETTING THE NEAREST ELEMENT ###
    def getNearestElementsOfTagDirect   (self,TAG ):
        elements = self.getElementsOfTagDirect(TAG)
        self.getNearestElements(elements)
    def getNearestElementsOfTypeDirect  (self,TYPE):
        elements = self.getElementsOfTypeDirect(TYPE)
        return self.getNearestElements(elements)

    ### GETTING DIRECTION TO ANOTHER ELEMENT ###
    def getNearestElements  (self,elements):
        distance = -1
        selected = []

        for x in range(len(elements)):
            px , py  = elements[x].getPosition()
            local_distance = math.sqrt(px*px+py*py)
            if distance == -1 or local_distance < distance:
                distance = local_distance
                selected = [elements[x]]
            elif(local_distance == distance:
                selected.append(elements[x])
        return selected
    def getToElementAngle   (self,element ):
        XP,YP = element.getPosition()
        X , Y = self.getPosition()

        self.FT1 = True
        DX = XP-X # 446
        DY = YP-Y

        cuadrante_primero = math.asin(DX/math.sqrt(DY*DY+DX*DX))/math.pi*(180)

        if   (DY >= 0 and DX >= 0):
            cuadrante_final = cuadrante_primero
        elif (DY < 0 and DX >= 0):
            cuadrante_final = 2*(90-cuadrante_primero) + cuadrante_primero
        elif (DY < 0 and DX < 0):
            cuadrante_final = cuadrante_primero - (2 * (cuadrante_primero+90) ) + 360
        elif (DY >= 0 and DX < 0):
            cuadrante_final = cuadrante_primero
        else:
            cuadrante_final = cuadrante_primero

        if (cuadrante_final < 0):
            cuadrante_final += 360

        return cuadrante_final
    def getToElementDistance(self,element):
        myx,myy = self.getCenterPosition()
        elx,ely = element.getCenterPosition()
        dx      = abs(myx - elx)
        dy      = abs(myy - ely)
        distance= math.sqrt(dx*dx+dy*dy)
        return distance

    def plu           (self,Events):
        pass
    def pgu           (self,Screen):
        pass

    ### HITTING MANAGMENT ###
    def hitTest      (self,element2,show = False):
        """
        @type element2: Element
        """

        ##### GETTING DATA #####
        MY_X, MY_Y = self.getPosition()
        MY_W, MY_H = self.getDimensions()
        MYX2, MYY2 = MY_X + MY_W, MY_Y + MY_H

        E2_X, E2_Y = element2.getPosition()
        E2_W, E2_H = element2.getDimensions()
        E2X2, E2Y2 = E2_X + E2_W, E2_Y + E2_H

        COLLISIONS = []
        ##### COLLISION LOGIC #####

        ##### PART 1 OF 4 #####
        if (MY_Y >= E2_Y and MY_Y <= E2Y2): #E
            conditionA = (MY_X <= E2_X and MYX2 >= E2X2)
            conditionB = (MY_X >= E2_X and MYX2 <= E2X2)
            conditionC = (MY_X > E2_X and MY_X < E2X2)
            conditionD = (MYX2 > E2_X and MYX2 < E2X2)

            if   (conditionA):
                data = {"COL":Collide.UP,"DIS":E2_W}
                COLLISIONS.append(data)
            elif (conditionB):
                data = {"COL":Collide.UP,"DIS":MY_W}
                COLLISIONS.append(data)
            elif (conditionC):
                dis = E2X2 - MY_X
                data = {"COL":Collide.UP,"DIS":dis}
                COLLISIONS.append(data)
            elif (conditionD):
                dis = MYX2 - E2_X
                data = {"COL":Collide.UP,"DIS":dis}
                COLLISIONS.append(data)

        ##### PART 2 OF 4 #####
        if (MYY2 >= E2_Y and MYY2 <= E2Y2): #F
            conditionA = (MY_X <= E2_X and MYX2 >= E2X2)
            conditionB = (MY_X >= E2_X and MYX2 <= E2X2)
            conditionC = (MY_X > E2_X and MY_X < E2X2)
            conditionD = (MYX2 > E2_X and MYX2 < E2X2)

            if   (conditionA):
                data = {"COL":Collide.DOWN,"DIS":E2_W}
                COLLISIONS.append(data)
            elif (conditionB):
                data = {"COL":Collide.DOWN,"DIS":MY_W}
                COLLISIONS.append(data)
            elif (conditionC):
                dis = E2X2 - MY_X
                data = {"COL":Collide.DOWN,"DIS":dis}
                COLLISIONS.append(data)
            elif (conditionD):
                dis = MYX2 - E2_X
                data = {"COL":Collide.DOWN,"DIS":dis}
                COLLISIONS.append(data)

        ##### PART 3 OF 4 #####
        if (MY_X >= E2_X and MY_X <= E2X2): #G
            conditionA = (MY_Y <= E2_Y and MYY2 >= E2Y2)
            conditionB = (MY_Y >= E2_Y and MYY2 <= E2Y2)
            conditionC = (MY_Y > E2_Y and MY_Y < E2Y2)
            conditionD = (MYY2 > E2_Y and MYY2 < E2Y2)

            if   (conditionA):
                data = {"COL":Collide.LEFT,"DIS":E2_H}
                COLLISIONS.append(data)
            elif (conditionB):
                data = {"COL":Collide.LEFT,"DIS":MY_H}
                COLLISIONS.append(data)
            elif (conditionC):
                dis = E2Y2 - MY_Y
                data = {"COL":Collide.LEFT,"DIS":dis}
                COLLISIONS.append(data)
            elif (conditionD):
                dis = MYY2 - E2_Y
                data = {"COL":Collide.LEFT,"DIS":dis}
                COLLISIONS.append(data)

        ##### PART 4 OF 4 #####
        if (MYX2 >= E2_X and MYX2 <= E2X2):
            conditionA = (MY_Y <= E2_Y and MYY2 >= E2Y2)
            conditionB = (MY_Y >= E2_Y and MYY2 <= E2Y2)
            conditionC = (MY_Y > E2_Y and MY_Y < E2Y2)
            conditionD = (MYY2 > E2_Y and MYY2 < E2Y2)

            if   (conditionA):
                data = {"COL":Collide.RIGHT,"DIS":E2_H}
                COLLISIONS.append(data)
            elif (conditionB):
                data = {"COL":Collide.RIGHT,"DIS":MY_H}
                COLLISIONS.append(data)
            elif (conditionC):
                dis = E2Y2 - MY_Y
                data = {"COL":Collide.RIGHT,"DIS":dis}
                COLLISIONS.append(data)
            elif (conditionD):
                dis = MYY2 - E2_Y
                data = {"COL":Collide.RIGHT,"DIS":dis}
                COLLISIONS.append(data)

        #### GETING PERCENTAJES ####
        total = 0
        for x in range(len(COLLISIONS)):
            total += COLLISIONS[x]["DIS"]

        for x in range(len(COLLISIONS)):
            actual_per = float(COLLISIONS[x]["DIS"]) / float(total) * 100.0
            COLLISIONS[x] = {"COL":COLLISIONS[x]["COL"],"DIS":COLLISIONS[x]["DIS"],"PER":actual_per}


        return COLLISIONS
    def getMaxCollide(self,element              ):
        collide = self.hitTest(element)
        max    = 0
        values = []

        for x in range(len(collide)):
            if (collide[x]["DIS"] > max):
                values = [collide[x]]
                max = collide[x]["DIS"]
            elif (collide[x]["DIS"] == max):
                values.append(collide[x])

        return values

    ### GETTING NETA X AND NETA Y POSITIONS
    def getNetaXPosition(self):
        return self.__netaXposition
    def getNetaYPosition(self):
        return self.__netaYposition

    def updateSurface(self,surfaceStructure):
        pass

    ### UPDATING FUNCTIONS ###
    def logic_update  (self,EVENTS):
        self.__netaXposition = self.GetX() - self.__CAM["x"]
        self.__netaYposition = self.GetY() - self.__CAM["y"]
        self.plu(EVENTS)
    def graphic_update(self,SCREEN):

        SCREEN.blit(self.surface,(self.__netaXposition,self.__netaYposition))
        self.pgu(SCREEN)
