__author__ = 'newtonis'

import pygame
import math
class imageTypes:
    LOAD_IMAGE,      \
    ROTATED_SURFACE, \
    ZOOM_SURFACE,    \
    SCALE_SURFACE,   \
    REP_IMAGE,       \
    LINE,            \
    CIRCLE,          \
    GEOLIST,         \
    FLIPSURFACE,     \
    BACKGROUND,      \
    BORDER,          \
    ROTATION,        \
    RADAR            \
    = range(13)

LoadedImages = []
reference    = 0

def addReference():
    global reference
    reference += 1
    return reference


def Load              (directory         ):
    return {"type":imageTypes.LOAD_IMAGE,"directory":directory,"reference":addReference()}
def LoadZoom          (directory,zoom    ):
    image = pygame.image.load("data/images/"+directory)
    iw,ih = image.get_size()
    w = iw*zoom
    h=  ih*zoom

    data = {"type":imageTypes.ZOOM_SURFACE,"w":w,"h":h,"structure":Load(directory),"reference":addReference()}

    return data
def LoadScale         (directory,scale   ):
    return {"type":imageTypes.ZOOM_SURFACE,"w":scale[0],"h":scale[1],"structure":Load(directory),"reference":addReference()}
def LoadFlip          (directory,A,B     ):
    return {"type":imageTypes.FLIPSURFACE,"w":A,"h":B,"structure":Load(directory),"reference":addReference()}
def LoadRep           (directory,RX,RY   ):
    return {"type":imageTypes.REP_IMAGE,"structure":Load(directory),"w":RX,"h":RY,"reference":addReference()}

def generateScale     (structure,w,h       ):
    return {"type":imageTypes.ZOOM_SURFACE,"w":w,"h":h,"structure":structure,"reference":addReference()}
def generateFlip      (structure,A,B       ):
    return {"type":imageTypes.FLIPSURFACE,"w":A,"h":B,"structure":structure,"reference":addReference()}
def generateRep       (structure,RX,RY     ):
    return {"type":imageTypes.REP_IMAGE,"structure":structure,"w":RX,"h":RY,"reference":addReference()}
def generateBackground(color,size          ):
    return {"type":imageTypes.BACKGROUND,"color":color,"w":size[0],"h":size[1],"reference":addReference()}
def addBorder         (structure,color,b1= 1,b2=1,b3=1,b4=1):
    return {"type":imageTypes.BORDER,"color":color,"reference":addReference(),"b1":b1,"b2":b2,"b3":b3,"b4":b4,"structure":structure}
def generateRotation  (structure,rotation  ):
    return {"type":imageTypes.ROTATION,"structure":structure,"angle":rotation,"reference":addReference()}
def generateScaleZoom (structure,angle,zoom):
    return {"type":imageTypes.SCALE_SURFACE,"structure":structure,"angle":angle,"zoom":zoom,"reference":addReference()}
def generateRadar     (color,alpha,distanceTo):
    return {"type":imageTypes.RADAR,"distance":distanceTp,"color":color,"alpha":alpha,"reference":addReference()}

def GetImageByStructure(structure):
    global LoadedImages

    for x in range(len(LoadedImages)):
        if (LoadedImages[x]["reference"] != None):
            if (LoadedImages[x]["reference"] == structure["reference"]):
                return LoadedImages[x]["image"]

    if (structure["type"] == imageTypes.LOAD_IMAGE):
        image = getSurface(structure)
    elif (structure["type"] == imageTypes.REP_IMAGE):
        image =  getRepSurface(structure)
    elif (structure["type"] == imageTypes.ZOOM_SURFACE):
        image = getZoomSurface(structure)
    elif (structure["type"] == imageTypes.ROTATED_SURFACE):
        image = getRotatedSurface(structure)
    elif (structure["type"] == imageTypes.FLIPSURFACE):
        image  = getFlipSurface(structure)
    elif (structure["type"] == imageTypes.BACKGROUND):
        image = getBackground(structure)
    elif (structure["type"] == imageTypes.BORDER):
        image = getBorder(structure)
    elif (structure["type"] == imageTypes.ROTATION):
        image = getRotation(structure)
    elif (structure["type"] == imageTypes.SCALE_SURFACE):
        image = getScaleZoom(structure)
    elif (structure["type"] == imageTypes.RADAR):
        image = getRadarSurface(structure)

    LoadedImages.append( {"image":image , "reference":structure["reference"]} )

    return image

def getSurface         (structure):
    '''
    global loadedImages
    for x in range(len(loadedImages)):
        if (loadedImages[x]["type"] == imageTypes.LOAD_IMAGE):
            if (loadedImages[x]["directory"] == structure["directory"]):
                return loadedImages[x]["image"]
    '''

    image = pygame.image.load("data/images/"+structure["directory"])

    return image
def getRepSurface      (structure):
    image = GetImageByStructure(structure["structure"])

    W,H = image.get_size()

    newSurface = pygame.surface.Surface((structure["w"]*W,structure["h"]*H))

    for x in range(W):
        for y in range(H):
            newSurface.blit(image,(W*x,H*y))

    return newSurface
def getZoomSurface     (structure):
    image = GetImageByStructure(structure["structure"])
    return pygame.transform.scale(image,(int(structure["w"]),int(structure["h"])))
def getScaleZoom       (structure):
    image = GetImageByStructure(structure["structure"])
    return pygame.transform.rotozoom(image,structure["angle"],structure["zoom"])
def getRotatedSurface  (structure):
    surface_dir = structure["structure"]

    image = GetImageByStructure(structure["structure"])

    return pygame.transform.rotate(image,(structure["angle"]))
def getFlipSurface     (structure):
    image = GetImageByStructure( structure["structure"] )

    return pygame.transform.flip(image,structure["w"],structure["h"])
def getBackground      (structure):
    surface = pygame.surface.Surface((structure["w"],structure["h"]))
    surface.fill(structure["color"])
    return surface
def getBorder          (structure):
    image = GetImageByStructure(structure["structure"])
    from gui import add_border
    final = add_border.add_border(image,structure["color"],structure["b1"],structure["b2"],structure["b3"],structure["b4"])
    return final
def getRotation        (structure):
    image = GetImageByStructure(structure["structure"])
    return pygame.transform.rotate(image,structure["angle"])
def getRadarSurface    (structure):
    iteracion = pygame.time.get_ticks()

    angle = iteracion % 100 / 360;

    surface = pygame.surface.Surface((structure["distanceTo"]*2,structure["distanceTo"]*2),32,pygame.SRCALPHA)
    surface.convert_alpha()

    surfaceB = pygame.surface.Surface((structure["distanceTo"]*2,structure["distanceTo"]*2),32,pygame.SRCALPHA)

    pygame.draw.circle(surfaceB, structure["color"],(0,0),structure["distanceTo"])

    surface.blit(surfaceB)
    pygame.draw.line(surface,(0,0,0),(structure["distanceTo"],structure["distanceTo"]),math.sin(math.radians(angle))*structure["distanceTo"],math.sin(math.radians(angle))*structure["distanceTo"])

    return surface
