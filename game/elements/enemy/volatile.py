__author__ = 'ariel'

import enemy
from load_data.images.enemies import volatile_enemy_01

class volatile(enemy.Enemy):
    def __init__(self):
        self.__FOT = 0
        self.__aceleration = 0

    def splu(self):
        pass