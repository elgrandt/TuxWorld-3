#Edicion: 1
#Por: Dylan
#Cree el sistema para crear la pantalla, junto con el sistema de actualizacion de eventos y puse para que la pantalla sea redimencionable y agregue algunos comandos basicos
#Edicion: 2
#Por: Ariel
#agrege modificaciones para el cambio cursor 
#Edicion: 3
#Por: Dylan
#Agregue la posibilidad de poner pantalla completa con la tecla F11 del teclado
#Edicion 4
#Por Ariel
#modificaciones para incluir la presentacion
#Edicion 5
#Por Dylan
#Agregue los comandos para cuando termina la presentacion y para cuando inicia el juego

import pygame,events
import status_cur
from gui import MenuActions
import presentation
from Tkinter import Tk
from utils import GameStatus

TkinterTest = Tk()
 
class Main:
    def __init__(self):
        self.CLOCK      = pygame.time.Clock()
        self.FRECUENCY  = 40
        self.ScreenSize = [800,600]
        self.Screen     = pygame.display.set_mode(self.ScreenSize,pygame.RESIZABLE)
        self.STATUS     = GameStatus.PRESENTATION


        self.Finished      = False
        self.Fullscreen    = False
        self.Events        = events.events()
        self.CurrentsAreas = []
        self.LastSize      = [0,0]
        pygame.display     . set_caption("Tux world 3")
        status_cur         . init()
        
        presentationA = presentation.Presentation()
        self.CurrentsAreas.append(presentationA)
        
        self.PRESENTATION = presentationA
        
        while not self.Finished:
            self.Update()
       
    def Update(self):
        Commands = []
        pygame.display.update()
        self.Screen.fill((255,255,255))
        
        self.Events.update_keyboard(pygame.key.get_pressed())
        self.Events.update_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        if self.Events.keyboard[pygame.K_F11]:
            if not self.Fullscreen:
                self.Fullscreen = True
                self.LastSize = [self.ScreenSize[0],self.ScreenSize[1]]
                self.ScreenSize = TkinterTest.maxsize()
                self.Screen = pygame.display.set_mode(self.ScreenSize,pygame.RESIZABLE|pygame.FULLSCREEN)
            else:
                self.Fullscreen = False
                self.ScreenSize = [self.LastSize[0],self.LastSize[1]]
                self.Screen = pygame.display.set_mode(self.ScreenSize,pygame.RESIZABLE)
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                Commands.append("Quit")
            if Event.type == pygame.VIDEORESIZE:
                self.ScreenSize = Event.dict['size']
                if self.Fullscreen:
                    self.Screen = pygame.display.set_mode(self.ScreenSize,pygame.RESIZABLE|pygame.FULLSCREEN)
                else:
                    self.Screen = pygame.display.set_mode(self.ScreenSize,pygame.RESIZABLE)
        
        for q in range(len(self.CurrentsAreas)):
            self.CurrentsAreas[q].graphic_update(self.Screen)
            self.CurrentsAreas[q].logic_update(self.Events)

        status_cur.update()
        
        for q in Commands:
            self.InterpreteCommands(q)
        
        self.GameLogic()
        self.CLOCK.tick(self.FRECUENCY)

    def InterpreteCommands(self,Command):
        if Command == "Quit":#Comando para salir
            self.Finished = True
        elif Command == "Restart":#Comando para reiniciar el juego
            Main()
            self.Finished = True
        else:
            pass
            
    def GameLogic(self):
        if (self.STATUS == GameStatus.PRESENTATION):
            if (self.PRESENTATION.getAction() == MenuActions.STARTGAME):
                self.STATUS = GameStatus.GAMEINIT
                self.startGame()
                
        elif (self.STATUS == GameStatus.GAMEINIT):
            pass

    def startGame(self):
        pass

Main()