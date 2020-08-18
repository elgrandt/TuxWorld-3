#Edicion 1
#Por Dylan
#Creando este archivo para que sea mas facil el manejo de la base de datos de lenguages
#Escriba el comando Ingresar para ingresar una traduccion a la base de datos, Escriba el comando Remover para remover una traduccion de la base de datos y escriba el comando ShowAll para ver toda base de datos

import gui.DatabaseFunctions as dat

def Consultar():
    Action = raw_input("Accion (Ingresar,Remover,ShowAll): ")
    
    if Action == "Ingresar" or Action == "ingresar" or Action == "1":
        dat.InsertWord()
    elif Action == "Remover" or Action == "remover" or Action == "2":
        dat.DeleteWord()
    elif Action == "ShowAll" or Action == "showall" or Action == "3":
        dat.ShowAll()
    else:
        print "Error de interpretacion"
        Consultar()

Consultar()