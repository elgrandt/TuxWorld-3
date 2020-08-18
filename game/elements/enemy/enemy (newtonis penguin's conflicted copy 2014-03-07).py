from game.elements import element
import math
import random
import pygame

def reduct90(angle):
    if (angle > 90):
        while (angle > 90):
            angle -= 90
    elif (angle < 0):
        while (angle < 0):
            angle += 90
    return angle

def getDistance(angle):
    reduct = reduct90(angle)

    return 45 - reduct

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
        self.__Direction = "Random"
        self.__Inteligent = False
        self.UpdateSurface(Surface)
        self.__unabletime = 0

    def setInitialAngle(self,angle):
        self.__Angle = angle
    def SetInteligent(self,Distance):
        self.__Inteligent = Distance
    def SetForce(self,NewForce):
        self.__Force = NewForce
    def GetForce(self):
        return self.__Force
    def SetDirection(self,NewDir):
        self.__Direction = NewDir
        if self.__Direction == "Vertical":
            self.setInitialAngle(0)
        elif self.__Direction == "Horizontal":
            self.setInitialAngle(90)
        elif self.__Direction == "Random":
            self.setInitialAngle(random.randrange(360))
        
    def __move(self):
        self.SetX(self.GetX()+math.sin(math.radians(self.__Angle))*self.__Speed)
        self.SetY(self.GetY()+math.cos(math.radians(self.__Angle))*self.__Speed)

    def Rotar(self,side):
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
    
    def UpdateLimits(self):
        pass
    def searchForPlayer(self):
        if self.__Inteligent != False:
            Players = self.getNearestElementsOfTypeDirect("Player")
            if ( len(Players) > 0) :
                XP,YP = Players[random.randrange(len(Players))].getPosition()
                X,Y = self.getPosition()
                W,H = self.getDimensions()
                IX,IY = self.__Inteligent
                if X > XP-IX and X < XP+IX and Y > YP-IY and Y < YP+IY:

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
                        cudrante_final = cuadrante_primero

                    if (cuadrante_final < 0):
                        cuadrante_final += 360

                    self.setInitialAngle(cuadrante_final)

    def plu(self,EVENTS):
        self.__move()
        self.UpdateLimits()

        Elements = self.getElementsOfTagDirect("Phisical")
        for x in range(len(Elements)):
            hits = self.getMaxCollide(Elements[x])
            for y in range(len(hits)):
                self.Rotar(hits[y])
            if (len(hits) > 0):
                self.__move()
                if Elements[x].isType("Player"):
                    self.RemoveEnergy(self.__Force)

        if self.__Inteligent != False:
            if (self.__unabletime == 0):
                self.searchForPlayer()
            else:
                self.__unabletime -= 1

class LimitsEnemy(Enemy):
    def init2(self,x,y,Surface,Limits):
        self.init(x, y, Surface)
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