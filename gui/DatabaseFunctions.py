"""
Database: Lenguages
Columnas = Spanish, English
"""
#Edicion 1
#Por: Dylan
#Creando la funcion InsertWord que podes ingresar cualquier palabra a la base de datos, por consola.
#Creando la funcion GetWord que es la que se va a usar para obtener la palabra por medio de su comando y devuelve la palabra segun el idioma obtenido por la funcion GetLenguage
#Creando la funcion DeleteWord que permite borrar la palabra con el comando escrito por consola
#Creando la funcion ShowAll que muestra en consola toda la base de datos con un esquema medio choto

import sqlite3

def InsertWord():
    Conection = sqlite3.connect("data/databases/lenguages.db")
    Cursor = Conection.cursor()
    Command = raw_input("Command: ")
    Spanish = raw_input("Spanish: ")
    English = raw_input("English: ")
    Cursor.execute("INSERT INTO Lenguages VALUES (?,?,?)",(Spanish,English,Command))
    Conection.commit()
    Conection.close()
    print "Datos ingresados correctamente"

def GetWord(Word):
    Conection = sqlite3.connect("data/databases/lenguages.db")
    Cursor = Conection.cursor()
    Cursor.execute("SELECT Spanish,English FROM Lenguages WHERE Command = '"+Word+"'")
    Data = Cursor.fetchone()
    Conection.commit()
    Conection.close()
    if Data != None:
        if GetLenguage() == "Spanish":
            return Data[0]
        elif GetLenguage() == "English":
            return Data[1]
    else:
        return "Error"

def DeleteWord():
    Word = raw_input("Command: ")
    Conection = sqlite3.connect("data/databases/lenguages.db")
    Cursor = Conection.cursor()
    Cursor.execute("DELETE FROM Lenguages WHERE Command = '"+Word+"'")
    Conection.commit()
    Conection.close()
    print "Datos Borrados"

def ShowAll():
    Conection = sqlite3.connect("data/databases/lenguages.db")
    Cursor = Conection.cursor()
    Cursor.execute("SELECT * FROM Lenguages")
    Data = Cursor.fetchall()
    Conection.commit()
    Conection.close()
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    print "Spanish | English | Command"
    print "---------------------------"
    for q in range(len(Data)):
        Print = ""
        for w in Data[q]:
            Print += w
            Print += " | "
        Print = Print[:len(Print)-3]
        print Print
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

def GetLenguage():
    return "English"