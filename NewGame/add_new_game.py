import sqlite3


def AddNewUserToDb(Name):
    Conection = sqlite3.connect("data/databases/Users.db")
    Cursor = Conection.cursor()
    NumAct = 0
    Cursor.execute("SELECT * FROM Usuarios")
    Data = Cursor.fetchall()
    for q in Data:
        if q[0] > NumAct:
            NumAct = q[0]
    NumAct += 1
    Conection.commit()
    Conection.close()
    InsertData(NumAct,Name)

def InsertData(NumAct,Name):
    Conection = sqlite3.connect("data/databases/Users.db")
    Cursor = Conection.cursor()
    import time
    FechaCompleta = time.localtime()
    Fecha = str(str(FechaCompleta.tm_mday)+"/"+str(FechaCompleta.tm_mon)+"/"+str(FechaCompleta.tm_year))
    Cursor.execute("""INSERT INTO Usuarios VALUES (?,?,?,?)""",(NumAct,Name,Fecha,"0"))
    Conection.commit()
    Conection.close()


def ShowAll():
    Conection = sqlite3.connect("data/databases/Users.db")
    Cursor = Conection.cursor()
    Cursor.execute("SELECT * FROM Usuarios")
    Data = Cursor.fetchall()
    Conection.commit()
    Conection.close()
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    print "ID | Nombre | Fecha de creacion | Nivel actual"
    print "---------------------------"
    for q in range(len(Data)):
        Print = ""
        for w in Data[q]:
            Print += str(w)
            Print += " | "
        Print = Print[:len(Print)-3]
        print Print
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

def GetAll():
    Conection = sqlite3.connect("data/databases/Users.db")
    Cursor = Conection.cursor()
    Cursor.execute("SELECT * FROM Usuarios")
    Data = Cursor.fetchall()
    Conection.commit()
    Conection.close()
    return Data

def DeleteUser(Name):
    Conection = sqlite3.connect("data/databases/Users.db")
    Cursor = Conection.cursor()
    Cursor.execute("DELETE FROM Usuarios WHERE Nombre = '"+Name+"'")
    Conection.commit()
    Conection.close()
    ShowAll()