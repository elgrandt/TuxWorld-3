

INC_RED   = 0
INC_GREEN = 1
INC_BLUE  = 2
DEC_RED   = 3
DEC_GREEN = 4
DEC_BLUE  = 5

class color:
    __MIN    = 0
    __MAX    = 0
    __ACTUAL = 0
    
    def __init__(self,MIN = 0,MAX = 255,ACTUAL = 0):
        self.__MIN    = MIN
        self.__MAX    = MAX
        self.__ACTUAL = ACTUAL
    def min(self):
        return self.__MIN
    
    def max(self):
        return self.__MAX

    def set_min(self,MIN):
        self.__MIN = MIN
        if (self.__ACTUAL < self.__MIN):
            self.__ACTUAL = self.__MIN
            
    def set_max(self,MAX):
        self.__MAX = MAX
        if (self.__ACTUAL > self.__MAX):
            self.__MAX = self.__ACTUAL
       
    def set_actual(self,ACTUAL):
        self.__ACTUAL = ACTUAL 
    
    def get_actual(self):
        return self.__ACTUAL
    
    def INC(self,SPEED):
        if (self.__ACTUAL < (self.__MAX+1) - SPEED):
            self.__ACTUAL += SPEED
            return False
        else:
            return True
        
    def DEC(self,SPEED):
        if (self.__ACTUAL >= self.__MIN + SPEED):
            self.__ACTUAL -= SPEED
            return False
        else:
            return True
        
class cBackground:
    __RED    = color()
    __GREEN  = color()
    __BLUE   = color() 
    __SPEED  = 1
    __ORDER  = [INC_RED,INC_BLUE,DEC_RED,INC_GREEN,DEC_BLUE,DEC_GREEN]
    __ACTUAL = 0
    
    def __init__(self):
        pass
    
    def resetOrder(self):
        self.__ORDER = []
        
    def addToOrder(self,STAGE):
        self.__ORDER.append(STAGE)
    
    def set_min_red(self,MIN):
        self.__RED.set_min(MIN)
    
    def set_max_red(self,MAX):
        self.__RED.set_max(MAX)
        
    def set_min_green(self,MIN):
        self.__GREEN.set_min(MIN)
        
    def set_max_green(self,MAX):
        self.__GREEN.set_max(MAX)
        
    def set_min_blue(self,MIN):
        self.__BLUE.set_min(MIN)
        
    def set_max_blue(self,MAX):
        self.__BLUE.set_max(MAX)
        
    def update(self):
        if (len(self.__ORDER) == 0):
            return 0
        
        CURRENT = self.__ORDER[self.__ACTUAL]
        
        NEXT    = False
        if   (CURRENT == INC_RED  ):
            NEXT = self.__IncRed()
        elif (CURRENT == INC_BLUE ):
            NEXT = self.__IncBlue()
        elif (CURRENT == INC_GREEN):
            NEXT = self.__IncGreen()
        elif (CURRENT == DEC_RED  ):
            NEXT = self.__DecRed()
        elif (CURRENT == DEC_BLUE ):
            NEXT = self.__DecBlue()
        elif (CURRENT == DEC_GREEN):
            NEXT = self.__DecGreen()
        
        if (NEXT):
            self.__Next()
    
    def __IncRed(self):
        return self.__RED.INC(self.__SPEED)
            
    def __DecRed(self):
        return self.__RED.DEC(self.__SPEED)
    
    def __IncBlue(self):
        return self.__BLUE.INC(self.__SPEED)
        
    def __DecBlue(self):
        return self.__BLUE.DEC(self.__SPEED)
            
    def __IncGreen(self):
        return self.__GREEN.INC(self.__SPEED)
            
    def __DecGreen(self):
        return self.__GREEN.DEC(self.__SPEED)
    
    def __Next(self):
        if (self.__ACTUAL < len(self.__ORDER)-1):
            self.__ACTUAL += 1
        else:
            self.__ACTUAL = 0
        
    def GetColor(self):
        return (self.__RED.get_actual(),self.__GREEN.get_actual(),self.__BLUE.get_actual())
    
    def SetSpeed(self,SPEED):
        self.__SPEED = SPEED