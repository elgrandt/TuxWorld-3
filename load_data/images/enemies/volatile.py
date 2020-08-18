
import glob
import pygame

from load_data.images.load import Load

volatile_enemy_01 = []

files = glob.glob("data/images/enemigos/*")

for x in range(len(files)):
    image = Load(files[x])
    volatile_enemy_01.append(image)

del files