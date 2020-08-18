import math

def encriptar(archivo):
    nuevo = ""
    for q in range(len(archivo)):
        actual = archivo[q]
        ascii = ord(actual)
        new = ascii * ascii
        new = new+1
        nuevo += ","+str(new)
    return nuevo

def finalizar(numero):
    new = int(numero)
    new = new-1
    new = int(math.sqrt(new))
    new = chr(new)
    return new

def desencriptar(encriptado):
    numero = ""
    numeros = []
    for q in range(len(encriptado)):
        actual = encriptado[q]
        if actual == ",":
            if numero != "":
                numeros.append(numero)
            numero = ""
        else:
            numero += actual
    if numero != "":
        numeros.append(numero)
    final = ""
    for q in numeros:
        final += finalizar(q)
    return final