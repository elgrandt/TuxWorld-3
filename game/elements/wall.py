import element,pygame
import load_data.images as img
from load_data.images import load

class directions:
    HORIZONTAL = 0
    VERTICAL   = 1


class Wall(element.Element):
    def __init__(self,x,y,image = img.Wall,distance = 3,direction = directions.HORIZONTAL):
        self.startWall(x,y,image,distance,direction)

    def startWall(self,x,y,image,distance,direction):
        ### SETTING ELEMENTS VARIABLES ###
        self.SetPosition     ((x,y))
        self.start           ()
        self.addTag          ("Wall")
        self.setType         ("Default wall")
        self.setPhisicElement()

        if (direction == directions.VERTICAL):
            image = load.generateRotation(image,90)
            structure = load.generateRep(image,1,distance)
        else:
            structure = load.generateRep(image,distance,1)

        self.UpdateSurface(structure)

class ClassicWall(Wall):
    def __init__(self,x,y,distance,direction):
        self.startWall(x,y,img.Wall,distance,direction)
