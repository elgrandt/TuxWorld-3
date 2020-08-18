
#Edicion: 1
#Por: Ariel

#Para testear la presentacion


import pygame
import events
import presentation

class MainGame:
    SCREEN = pygame.display.set_mode((800,600))
    EVENTS = events.events()
    CLOCK  = pygame.time.Clock()
    SCALE  = 1
    LOOPS  = 0
    STAGE  = []
    FREC   = 40  
    EXIT   = False
    
    def __init__(self):
        pres = presentation.Presentation()

        self.STAGE.append(pres)
    
    def logic_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.EXIT = True
        
        self.EVENTS.update_keyboard(pygame.key.get_pressed())
        self.EVENTS.update_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        
        for x in range(len(self.STAGE)):
            self.STAGE[x].logic_update(self.EVENTS)

    def graphic_update(self):
        self.SCREEN.fill((255,255,255))
        for x in range(len(self.STAGE)):
            self.STAGE[x].graphic_update(self.SCREEN)
        
        pygame.display.update()
        
    def update(self):
        self.graphic_update()
        if (self.LOOPS % self.SCALE == 0):
            self.logic_update()
            
        self.LOOPS += 1
        self.CLOCK.tick(self.FREC)
        
    def Exit(self):
        return self.EXIT
    
def main():
    mainGame = MainGame()
    
    while True:
        mainGame.update()
        if mainGame.Exit():
            break
main()