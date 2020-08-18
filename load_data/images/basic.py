__author__ = 'newtonis'


from load import *

ContinueMenu = Load("Continue.png")
error_elemento = Load("Error.png")
ClassicEnemy = LoadScale("enemigos/windows.png",(50,50))


Wall = Load("wall/paredTile.png")

Signal = Load("Signal.png")

Vacio = Load("Vacio.png")

def Load075(ruta):
    return generateScaleZoom(Load(ruta),0,0.75)

def getTuxImages():
    front = []
    back  = []
    walk  = []
    lwalk = []

    front.append(Load075("tux/tux1.png"           ))
    front.append(Load075("tux/tux_caminando1.png" ))
    front.append(Load075("tux/tux_caminando2.png" ))

    back .append(Load075("tux/tux2.png"))
    back .append(Load075("tux/tux2_caminando1.png"))
    back .append(Load075("tux/tux2_caminando1.png"))

    walk .append(Load075("tux/tux3_caminando1.png"))
    walk .append(Load075("tux/tux3_caminando2.png"))
    walk .append(Load075("tux/tux3_caminando3.png"))
    walk .append(Load075("tux/tux3_caminando4.png"))
    walk .append(Load075("tux/tux3_caminando5.png"))

    lwalk .append(generateFlip(Load075("tux/tux3_caminando1.png"),True,False))
    lwalk .append(generateFlip(Load075("tux/tux3_caminando2.png"),True,False))
    lwalk .append(generateFlip(Load075("tux/tux3_caminando3.png"),True,False))
    lwalk .append(generateFlip(Load075("tux/tux3_caminando4.png"),True,False))
    lwalk .append(generateFlip(Load075("tux/tux3_caminando5.png"),True,False))

    return {"front":front,"back":back,"walk":walk,"left-walk":lwalk}

tuxImages = getTuxImages()