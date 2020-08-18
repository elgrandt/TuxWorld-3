import Background
import pygame
import gui.add_border as add_border
from load_data.images import load

class ClassicBackground(Background.Background):
    def __init__(self,x,y,CantX,CantY,Color,Border=0):

        structure = load.generateBackground(Color,(50,50))

        final = load.addBorder(structure,(0,0,0),1,0,1,0)

        self.init(x, y, CantX, CantY, final)