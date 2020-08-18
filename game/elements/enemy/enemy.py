from game.elements import element
import math
import random
import pygame
import gui.Circle as Circle
import load_data.images as img

class AttackRanges:
    UNLIMITED, \
    CIRCLE, \
    RECTANGLE, \
    CUSTOM \
    = range(4)

class Directions:
    VERTICAL, \
    HORIZONTAL, \
    RANDOM \
    = range(3)


class Enemy(element.Element):
    def init(self,x,y,Surface):
        self.SetPosition([x,y])
        self.start()
        self.__Angle = 30
        self.__Speed = 5
        self.addTag          ("Enemy")
        self.addTag          ("Wall")
        self.addTag          ("Mobile")
        self.setType         ("Enemy default")
        self.setPhisicElement()
        self.__Force = 0
        self.UpdateSurface(Surface)
        self.__unabletime = 0
        self.FT1 = True
        self.__EnabledRange = False

    def setInitialAngle(self,angle   ):
        self.__Angle = angle
    def rotation       (self,angle   ):
        self.__Angle += angle
        if (self.__Angle >= 360):
            self.__Angle -= 360
    def SetForce       (self,NewForce):
        self.__Force = NewForce
    def SetSpeed       (self,Speed   ):
        self.__Speed = Speed
    def GetForce       (self         ):
        return self.__Force
    def InterpreteDirection(self,Str):
        if Str == "Vertical" or Str == "vertical":
            return Directions.VERTICAL
        elif Str == "Horizontal" or Str == "horizontal":
            return Directions.HORIZONTAL
        elif Str == "Random" or  Str == "random":
            return Directions.RANDOM
        else:
            return Directions.RANDOM
    def SetDirection   (self,NewDir   ):
        self.InterpreteDirection(NewDir)
        if NewDir == Directions.VERTICAL:
            self.setInitialAngle(0)
        elif NewDir == Directions.HORIZONTAL:
            self.setInitialAngle(90)
        elif NewDir == Directions.RANDOM:
            self.setInitialAngle(random.randrange(360))
        
    def __move         (self     ):
        self.SetX(self.GetX()+math.sin(math.radians(self.__Angle))*self.__Speed)
        self.SetY(self.GetY()+math.cos(math.radians(self.__Angle))*self.__Speed)

    def Rotar          (self,side):
        if side["COL"] == element.Collide.UP:
            self.__Angle = 180 - self.__Angle
            self.__unabletime = 40
        elif side["COL"] == element.Collide.LEFT:
            self.__Angle = self.__Angle + (180-self.__Angle)*2
            self.__unabletime = 40
        elif side["COL"] == element.Collide.DOWN:
            self.__Angle = 180 - self.__Angle
            self.__unabletime = 40
        elif side["COL"] == element.Collide.RIGHT:
            self.__Angle = self.__Angle + (180-self.__Angle)*2
            self.__unabletime = 40

    def plu(self,EVENTS ):
        self.splu(EVENTS)
        self.__move()

        Elements = self.getElementsOfTagDirect("Phisical")
        for x in range(len(Elements)):
            hits = self.getMaxCollide(Elements[x])
            for y in range(len(hits)):
                self.Rotar(hits[y])
            if (len(hits) > 0):
                self.__move()
                if Elements[x].isType("Player"):
                    self.RemoveEnergy(self.__Force)

    def getAble    (self):
        return self.__unabletime == 0
    def reduceUnable(self):
        self.__unabletime -= 1
    def pgu(self,SCREEN):
        enemy4Player.pgu(self, SCREEN)


class enemy4Player(Enemy):
    def __init__(self):
        pass
    def startEnemy4Player(self):
        self.__rangeVisible = False
        self.__noRange = False
        self.ActAngle = 360
    def enableRangeVisible(self):
        self.__rangeVisible = True
    def setAttackRange         (self,type   ):
        self.__AttackType = type
        self.enableRangeVisible()
    def getNearestPlayerInRange(self        ):
        Players = self.getElementsOfTypeDirect("Player")
        for x in range(len(Players)-1,-1,-1):
            if (not self.isInRange(Players[x])):
                del Players[x]
        if (len(Players) == 0):
            return None
        return self.getNearestElements(Players)

    def searchForPlayer        (self        ):
        Players = self.getNearestPlayerInRange()
        if Players == None:
            if not self.__noRange:
                self.handleNoMoreRange()
                self.__noRange = True
            return None
        if len(Players) < 0:
            return None
        self.__noRange = False
        player  = Players [ random.randrange(len(Players)) ]
        angle   = self.getToElementAngle(player)
        distance= self.getToElementDistance(player)
        self    . handleSearching(angle,distance)

    def isInRange              (self,element):
        if (self.__AttackType["type"] == AttackRanges.UNLIMITED):
            return True
        elif (self.__AttackType["type"] == AttackRanges.CIRCLE):
            return self.handleCircularRange (element)
        elif (self.__AttackType["type"] == AttackRanges.RECTANGLE):
            return self.handleRectangleRange(element)
        elif (self.__AttackType["type"] == AttackRanges.CUSTOM):
            return self.handleCustomRange()

    def handleCircularRange    (self,element):
        print self.getToElementDistance(element)
        if (self.getToElementDistance(element) <= self.__AttackType["radius"]):
            return True
        else:
            return False
    def handleRectangleRange   (self,element):
        RX,RY = self.__AttackType["x"],self.__AttackType["y"]
        XP,YP = self.getCenterPosition()
        X,Y = element.getCenterPosition()
        W,H = self.getDimensions()
        IX,IY = self.__AttackType["width"] , self.__AttackType["height"]
        if X >= RX + XP-IX/2 and X <= RX + XP+IX/2 and Y >= RY + YP-IY/2 and Y <= RY + YP+IY/2:
            return True
        return False
    def handleCustomRange      (self,element):
        rectangles = self.__AttackType["rectangles"]
        for x in range(len(rectangles)):
            self.__AttackType["width"] = rectangles["width"]
            self.__AttackType["height"]= rectangles["height"]
            self.__AttackType["x"]     = rectangles["x"]
            self.__AttackType["y"]     = rectangles["y"]
            if (not self.handleRectangleRange(element)):
                return False
        return True

    def handleSearching   (self,angle,distance):
        pass

    def handleNoMoreRange(self):
        self.rotation(180)

    def splu(self, EVENTS):
        if (self.getAble()):
            self.searchForPlayer()
        else:
            self.reduceUnable()
        self.ssplu(EVENTS)

    def ssplu(self,EVENTS):
        pass

    def pgu(self,SCREEN):
        if (self.__rangeVisible):
            if (self.__AttackType["type"] == AttackRanges.RECTANGLE):
                self.handleRectangleSurface(SCREEN)
            elif (self.__AttackType["type"] == AttackRanges.CIRCLE):
                self.handleCircleSurface(SCREEN)
            elif (self.__AttackType["type"] == AttackRanges.CUSTOM):
                self.handleCustomSurface(SCREEN)

    def handleRectangleSurface(self,SCREEN):
        original_image = img.Signal

        if (self.ActAngle > 0 and self.ActAngle <= 90) or (self.ActAngle > 180 and self.ActAngle <= 270):
            im = pygame.transform.scale(im,(50,self.__AttackType["height"]/2))
        else:
            im = pygame.transform.scale(im,(50,self.__AttackType["width"]/2))
            im = pygame.transform.rotate(im,180)


        imag = pygame.transform.rotate(im,self.ActAngle)
        
        imva = pygame.transform.scale(img.Vacio,[self.__AttackType["width"],self.__AttackType["height"]])
        simva = imva.get_size()
        simag = imag.get_size()
        mid = [simva[0]/2,simva[1]/2]
        if self.ActAngle >= 0 and self.ActAngle < 90:
            Posi = [mid[0]-simag[0],mid[1]-simag[1]]
        elif self.ActAngle >= 90 and self.ActAngle < 180:
            Posi = [mid[0],mid[1]-simag[1]]
        elif self.ActAngle >= 180 and self.ActAngle < 270:
            Posi = mid
        elif self.ActAngle >= 270 and self.ActAngle <= 360:
            Posi = [mid[0]-simag[0],mid[1]]
        imva.blit(imag,Posi)
        
        Pos = [self.getPosition()[0]+self.getDimensions()[0]/2-self.__AttackType["width"]/2,self.getPosition()[1]+self.getDimensions()[1]/2-self.__AttackType["height"]/2]
        SCREEN.blit(imva,[Pos[0]-self.GetCamera()["x"],Pos[1]-self.GetCamera()["y"]])
        self.ActAngle -= 1
        if self.ActAngle <= 0:
            self.ActAngle = 360
    def handleCircleSurface   (self,SCREEN):
        pass
    def handleCustomSurface   (self,SCREEN):
        pass

class LimitsEnemy(Enemy):
    def SetLimits(self,Limits):
        self.__Limits = Limits
    def UpdateLimits(self):
        if self.__Limits != None:
            Len = 10
            Test1 = pygame.Surface((Len,self.__Limits[1][1]-self.__Limits[1][0]-2*Len))
            Test2 = pygame.Surface((self.__Limits[0][1]-self.__Limits[0][0]-Len*2,Len))
            El1 = element.Element()
            El1.start()
            El1.UpdateSurface(Test1)
            El1.SetPosition((self.__Limits[0][0],self.__Limits[1][0]+Len))
            
            El2 = element.Element()
            El2.start()
            El2.UpdateSurface(Test1)
            El2.SetPosition((self.__Limits[0][1]-Len,self.__Limits[1][0]+Len))
            
            El3 = element.Element()
            El3.start()
            El3.UpdateSurface(Test2)
            El3.SetPosition((self.__Limits[0][0]+Len,self.__Limits[1][0]))
            
            El4 = element.Element()
            El4.start()
            El4.UpdateSurface(Test2)
            El4.SetPosition((self.__Limits[0][0]+Len,self.__Limits[1][1]-Len))
            
            for q in self.getMaxCollide(El1):
                self.Rotar(q)
            for q in self.getMaxCollide(El2):
                self.Rotar(q)
            for q in self.getMaxCollide(El3):
                self.Rotar(q)
            for q in self.getMaxCollide(El4):
                self.Rotar(q)