
import pygame,events
import status_cur
from gui import MenuActions
from game.mygame import test_level
from Tkinter import Tk
from utils import GameStatus

TkinterTest = Tk()



class Main:
    def __init__(self):

        self.CLOCK      = pygame.time.Clock()
        self.FRECUENCY  = 50
        self.ScreenSize = [800,600]
        self.Screen     = pygame.display.set_mode(self.ScreenSize,pygame.RESIZABLE)
        self.STATUS     = GameStatus.PRESENTATION


        self.Finished      = False
        self.Fullscreen    = False
        self.Events        = events.events()
        self.CurrentsAreas = []
        self.LastSize      = [400,400]
        pygame.display     . set_caption("Tux world 3")
        status_cur         . init()
        
        self.CurrentsAreas.append(test_level())
        
        while not self.Finished:
            self.Update()
            if (self.Events.get_keyboard()[pygame.K_RETURN]):
                while (not self.Events.get_keyboard()[pygame.K_SPACE]):
                    pygame.event.get()
                    self.Events.update_keyboard(pygame.key.get_pressed())
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
            print Command
            
    def GameLogic(self):
        pass

    def startGame(self):
        pass

Main()