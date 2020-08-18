from game.elements.element import Element
from load_data.images import load
import pygame

class Background(Element):
    def init(self,x,y,CantX,CantY,structure):
        self.SetPosition([x,y])
        self.start()
        self.addTag("Background")
        self.setType("Background default")
        BaseSurface = load.generateRep(structure,CantX,CantY)


        self.UpdateSurface(BaseSurface)