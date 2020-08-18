import pygame
from load_data.cursors.pointer import *

cursor = None

def init():
    global cursor
    cursor = "arrow"

def set_pointer():
    global cursor
    cursor = "pointer"

def update():
    global cursor
    if (cursor == "arrow"):
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    elif (cursor == "pointer"):
        pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )
        
    cursor = "arrow"
   
