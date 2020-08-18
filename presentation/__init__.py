#edicion 1
#por: Ariel
#aca se encuentra la clase que maneja la presentacion con el fondo y las diferentes letras que aparecen

#edicion 2
#por: Dylan
#Aplicando el sistema de tradiccion

import autors
import background
import game_title
import pygame
from gui import Menu
from gui import MenuActions
import gui.DatabaseFunctions as dat
from load_data.images import misc
from NewGame import NewGame

class stageElement:
    def __init__(self,OBJECT,NAME,ID):
        self.__OBJECT = OBJECT
        self.__NAME = NAME
        self.__ID = ID

    def logic_update(self,EVENTS):
        self.__OBJECT.logic_update(EVENTS)

    def graphic_update(self,SCREEN):
        self.__OBJECT.graphic_update(SCREEN)

    def GetObject(self):
        return self.__OBJECT

    def GetName(self):
        return self.__NAME

    def GetID(self):
        return self.__ID

class Presentation:

    def __init__(self):
        self.__index = 0

        self.STAGE      = []
        self.BACKGROUND = background.Background()

        self.AddToStage(self.BACKGROUND,"Background")

        STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()
    
        TEXTOA     = dat.GetWord("presentacion parte 1")
        TEXTOB     = dat.GetWord("presentacion parte 2")
    
        self.LETRASA    = autors.autorEffect(TEXTOA,(STAGE_WIDTH / 2 - len(TEXTOA)*10,STAGE_HEIGHT / 2-15))
        self.LETRASB    = autors.autorEffect(TEXTOB,(STAGE_WIDTH / 2 - len(TEXTOB)*10,STAGE_HEIGHT / 2+15))
        
        self.AddToStage(self.LETRASA,"Autors A")
        self.AddToStage(self.LETRASB,"Autors B")
    
        self.LETRASA.StartMove()
        
        self.phrase    = "Authors"
        self.auxiliarA = 0
        
        self.__ACTION = MenuActions.NOSET
        
        self.subMenus = []
        self.__started = False
        self.__waitToUnclock = 0

    def EvaluateSkip(self,EVENTS):
        keyboard = EVENTS.get_keyboard()
        if (keyboard[pygame.K_RETURN] and not self.__started):
            self.skip()

    def skip(self):
        STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()

        self.RemoveFromStage("Autors A")
        self.RemoveFromStage("Autors B")

        self.phrase = "Game title is"

        self.GAME_NAME = game_title.GameTitle()
        self.GAME_NAME.set_position((0,0))
        self.GAME_NAME.set_position((STAGE_WIDTH / 2 - self.GAME_NAME.aumento/2,STAGE_HEIGHT / 2-self.GAME_NAME.H/2))

        self.GAME_NAME.skip()
        self.GAME_NAME.status = "End"

        self.AddToStage(self.GAME_NAME,"Game Name")

    def logic_update(self,EVENTS):
        for x in range(len(self.STAGE)):
            self.STAGE[x].logic_update(EVENTS)


        self.EvaluateSkip(EVENTS)
        if (self.phrase == "Authors"):
            if (self.LETRASA.End()):
                self.LETRASB.StartMove()
            if (self.LETRASB.End()):
                self.phrase = "Wait 2 quit"
                self.auxiliarA = 80
        elif (self.phrase == "Wait 2 quit"):
            self.auxiliarA -= 1
            if (self.auxiliarA == 0):
                self.LETRASA.QuitLetters()
                self.LETRASB.QuitLetters()
                
                self.phrase = "Game title start"
        elif (self.phrase == "Game title start"):
            STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()
            
            self.GAME_NAME = game_title.GameTitle()
            self.GAME_NAME.set_position((0,0))
            self.GAME_NAME.set_position((STAGE_WIDTH / 2 - self.GAME_NAME.aumento/2,STAGE_HEIGHT / 2-self.GAME_NAME.H/2))
            
            
            self.AddToStage(self.GAME_NAME,"Game Name")
            
            self.phrase = "Game title"
            self.auxiliarA = 40
        elif (self.phrase == "Game title"):
            self.auxiliarA -= 1
            if (self.auxiliarA == 0):
                self.RemoveFromStage("Autors A")
                self.RemoveFromStage("Autors B")

                self.GAME_NAME.start()
                self.phrase = "Game title is"
                
        elif (self.phrase == "Game title is"):
            if (self.GAME_NAME.status == "End"):
                self.__started = True
                print "Adding menu"
                self.phrase = "Menu"
                STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()

                submenu = Menu.Menu2((0,0))

                submenu.AddOption("Local", MenuActions.NOSET, {})
                submenu.AddOption("National", MenuActions.NOSET, {})
                submenu.AddOption("International", MenuActions.NOSET, {})
                submenu.StartOptions()
                submenu.addReturnButton(misc.back_arrow,MenuActions.CLOSEMENU,{})


                menu1 = Menu.Menu2((STAGE_WIDTH/2 - 150,STAGE_HEIGHT/2 - 150))
                menu1.AddOption(dat.GetWord("nueva partida"), MenuActions.STARTGAME , {})
                menu1.AddOption(dat.GetWord("cargar partida"), MenuActions.NOSET , {})
                menu1.AddOption(dat.GetWord("unirse a partida"), MenuActions.NOSET , {})
                menu1.AddOption(dat.GetWord("mejores puntajes"), MenuActions.OPENMENU , submenu)
                menu1.StartOptions()
                menu1.block()
                self.__waitToUnclock = 20

                self.AddToStage(menu1,"Menu principal")
                self.subMenus.append(menu1)
                
                self.MENU = menu1
        elif (self.phrase == "Menu"):
            if (self.__waitToUnclock > 1):
                self.__waitToUnclock -= 1
            else:
                self.__waitToUnclock -=1
                self.MENU.unblock()
            ToDo = self.MENU.getCurrentAction()

            self.evaluate(ToDo)

        elif (self.phrase == "Menu change"):
            STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()

            RightMenu = self.subMenus[len(self.subMenus)-1]
            LeftMenu  = self.subMenus[len(self.subMenus)-2]
            if (RightMenu.GetX() >= STAGE_WIDTH/2 - 150):
                RightMenu.moveLeft()
                LeftMenu.moveLeft()
            else:
                self.MENU = self.subMenus[len(self.subMenus)-1]
                self.phrase = "Menu"
                self.MENU.unblock()

        elif (self.phrase == "Menu return"):
            STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()

            RightMenu = self.subMenus[len(self.subMenus)-1]
            LeftMenu  = self.subMenus[len(self.subMenus)-2]

            if (LeftMenu.GetX() <= STAGE_WIDTH/2-150):
                RightMenu.moveRight()
                LeftMenu.moveRight()
            else:
                self.RemoveFromStage("Sub menu "+str(len(self.subMenus)-1))
                del self.subMenus[len(self.subMenus)-1]

                self.MENU = self.subMenus[len(self.subMenus)-1]
                self.MENU.unblock()
                self.phrase = "Menu"
        elif (self.phrase == "Create Game transition"):
            STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()

            form = self.GetStageReferenceByName("New game form")

            form.GetObject().Move(STAGE_WIDTH/2-form.GetObject().GetGlobalSize()[0]/2,10)

            self.phrase = "Create Game moving"
        elif (self.phrase == "Create Game moving"):
            self.MENU.moveLeft()

            form = self.GetStageReferenceByName("New game form")

            if (form.GetObject().GetMoving() == 0):
                self.phrase = "Create game finished"
        elif (self.phrase == "Create game finished"):

            form = self.GetStageReferenceByName("New game form")


            if (form.GetObject().ComeBack()):
                self.phrase = "Create game return"
                STAGE_WIDTH = pygame.display.get_surface().get_size()[0]

                form.GetObject().Move(STAGE_WIDTH+500,10)

        elif (self.phrase == "Create game return"):
            self.MENU.moveRight()
            STAGE_WIDTH = pygame.display.get_surface().get_size()[0]

            form = self.GetStageReferenceByName("New game form")

            if (self.MENU.GetX() >= STAGE_WIDTH/2-150):
                self.phrase = "Menu"
                self.MENU.unblock()

    def getAction(self):
        action = self.__ACTION
        self.action = MenuActions.NOSET
        return action
    
    def graphic_update(self,SCREEN):
        
        for x in range(len(self.STAGE)):
            self.STAGE[x].graphic_update(SCREEN)

    def evaluate(self,ToDo):

        action = ToDo["action"]
        if (action == MenuActions.NOSET):
            return 0

        if (action == MenuActions.OPENMENU):
            STAGE_WIDTH,STAGE_HEIGHT = pygame.display.get_surface().get_size()

            OPCIONES = ToDo["params"]

            OPCIONES.SetPosition((STAGE_WIDTH,STAGE_HEIGHT/2 - 150))
            OPCIONES.block()
            self.subMenus[len(self.subMenus)-1].block()

            self.subMenus.append(OPCIONES)

            self.AddToStage(OPCIONES,"Sub menu "+str(len(self.subMenus)-1))

            self.phrase = "Menu change"

        elif (action == MenuActions.CLOSEMENU):

            self.phrase = "Menu return"
            self.subMenus[len(self.subMenus)-1].block()
            self.subMenus[len(self.subMenus)-2].block()
        elif (action == MenuActions.STARTGAME):
            print "Starting game"
            self.phrase = "Create Game transition"

            newgame = NewGame()
            self.MENU.block()
            self.AddToStage(newgame,"New game form")
        else:
            self.__ACTION = action

    def AddToStage(self,element,name):
        element = stageElement(element,name,self.__index)
        self.STAGE.append(element)
        self.__index += 1

    def RemoveFromStage(self,name):
        index = self.GetStageIndexByName(name)
        if (index != None):
            del self.STAGE[ self.GetStageIndexByName(name) ]

    def GetStageIndexByName(self,name):
        for x in range(len(self.STAGE)):
            if (self.STAGE[x].GetName() == name):
                return x

    def GetStageReferenceByName(self,name):
        return self.STAGE[ self.GetStageIndexByName(name) ]