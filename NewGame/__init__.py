#Edicion 1
#Por Dylan
#Cree la clase NewGame que va a ser donde se ingrese el nombre del jugador que va a crear la partida

#Edicion 2
#Por Dylan
#Cree la funcion move que mueve todo el block de objetos hasta un punto determinado y pudiendo modificarle la velocidad

import pygame
from gui import Clasic
from gui import input_text
from load_data import fonts
from gui import DatabaseFunctions as dat
from gui import Button
from gui import MenuActions
from NewGame.add_new_game import AddNewUserToDb

class NewGame(Clasic.Clasic2):
    def __init__(self):
        self.__ACTION = MenuActions.NOSET
        self.Font = fonts.ubuntu_bold_graph(25)
        self.Input = input_text.text_input()
        self.Input.set_alpha_states(0.9, 1)
        self.Input.allowLetters()
        self.Input.allowNumbers()
        self.Input.set_show_text(dat.GetWord("aqui"))
        self.Input.set_background((0,175,255))
        self.Input.set_border_color((0,107,255))
        self.Input.set_border_size(2)
        self.Input.set_margin(6)


        self.Button = Button.Button(dat.GetWord("continuar"),(100,100,100),(0,0))
        
        self.ReturnButton = Button.Button(dat.GetWord("cancelar"),(200,200,200),(0,0))

        self.Moving = None
        self.Disf = pygame.display.get_surface().get_size()[0]/2+self.Input.surface.get_size()[0]
        self.original = self.Disf
        self.SpeedMove = 0
        Name = self.Font.render(dat.GetWord("ingresar nombre"),1,(0,0,0))
        self.GlobalSize = [self.Input.surface.get_size()[0], Name.get_size()[1]+10+self.Input.surface.get_size()[1]+10+self.Button.surface.get_size()[1]]
        self.DirMove = None
        self.Finished = False
    def graphic_update(self,Screen):
        if not self.Finished:
            GlobalButtonSize = self.Button.NormalSize[0]+10+self.ReturnButton.NormalSize[0]
            
            Name = self.Font.render(dat.GetWord("ingresar nombre"),1,(0,0,0))
            if self.Input.surface.get_size()[0] > Name.get_size()[0] and self.Input.surface.get_size()[0] > GlobalButtonSize:
                self.GlobalSize = [self.Input.surface.get_size()[0], Name.get_size()[1]+10+self.Input.surface.get_size()[1]+10+self.Button.NormalSize[1]]
            elif Name.get_size()[0] > self.Input.surface.get_size()[0] and Name.get_size()[0] > GlobalButtonSize:
                self.GlobalSize = [Name.get_size()[0], Name.get_size()[1]+10+self.Input.surface.get_size()[1]+10+self.Button.NormalSize[1]]
            elif GlobalButtonSize > self.Input.surface.get_size()[0] and GlobalButtonSize > Name.get_size()[0]:
                self.GlobalSize = [GlobalButtonSize, Name.get_size()[1]+10+self.Input.surface.get_size()[1]+10+self.Button.NormalSize[1]]
            GlobalTestSurface = pygame.Surface(self.GlobalSize)
            self.PosName = (Clasic.GetCenterPosition(Screen, Name)[0] + self.Disf,Clasic.GetCenterPosition(Screen, GlobalTestSurface)[1])
            Screen.blit(Name,self.PosName)
            self.PosInput = (Clasic.GetCenterPosition(Screen, self.Input.surface)[0] + self.Disf,Clasic.GetCenterPosition(Screen, GlobalTestSurface)[1]+Name.get_size()[1]+10)
            self.Input.set_position(self.PosInput)
            self.Input.graphic_update(Screen)
    
            TestSurface = pygame.Surface((GlobalButtonSize,self.Button.surface.get_size()[1]))
    
            self.ReturnButton.UpdatePosition((Clasic.GetCenterPosition(Screen, TestSurface)[0] + self.Button.NormalSize[0] + 10 + self.Disf,Clasic.GetCenterPosition(Screen, GlobalTestSurface)[1]+Name.get_size()[1]+10+self.Input.surface.get_size()[1]+10))
    
            self.Button.UpdatePosition((Clasic.GetCenterPosition(Screen, TestSurface)[0] + self.Disf,Clasic.GetCenterPosition(Screen, GlobalTestSurface)[1]+Name.get_size()[1]+10+self.Input.surface.get_size()[1]+10))
            self.Button.graphic_update(Screen)
            if self.Moving != None:
                if self.DirMove == None:
                    if self.Moving < self.Button.OriginalPosition[0]:
                        self.DirMove = "Izquierda"
                    elif self.Moving > self.Button.OriginalPosition[0]:
                        self.DirMove = "Derecha"
                else:
                    if self.DirMove == "Izquierda":
                        if self.Moving < self.Button.OriginalPosition[0]:
                            self.Disf -= self.SpeedMove
                        else:
                            if self.Moving != self.Button.OriginalPosition[0]:
                                self.SpeedMove = 1
                            else:
                                self.Moving = None
                                self.DirMove = None
                    elif self.DirMove == "Derecha":
                        if self.Moving > self.Button.OriginalPosition[0]:
                            self.Disf += self.SpeedMove
                        else:
                            if self.Moving != self.Button.OriginalPosition[0]:
                                self.SpeedMove = 1
                            else:
                                self.Moving = None
                                self.DirMove = None
                
                if self.Moving == self.Button.OriginalPosition[0]:
                    self.Moving = None
            self.ReturnButton.graphic_update(Screen)
    def logic_update(self,Events):
        if not self.Finished:
            self.Input.logic_update(Events)
            self.Button.logic_update(Events)
            self.ReturnButton.logic_update(Events)
            if self.Button.Pressed():
                AddNewUserToDb(self.Input.get_curent_text())
                self.Finished = True
    def Move(self,to,speed):
        self.SpeedMove = speed
        self.Moving = to
    
    def GetMoving(self):
        if self.Moving != None:
            return True
        else:
            return False

    def GetGlobalSize(self):
        return self.GlobalSize
    def ComeBack(self):
        return self.ReturnButton.Pressed()