import os
import sys
import random

import pygame

FPS = 60
mapp = 0
pygame.init()
size = WIDTH, HEIGHT = 2056, 1024
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
GRAVITY = 5

background_image_filename = 'image.jpg'


SCREEN_SIZE = (640, 480)

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.constants.RESIZABLE, 32)

background = pygame.image.load(background_image_filename).convert()

while True:

    pygame.display.update()
