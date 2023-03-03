import pygame
from parts_of_code.constantes import *

pygame.init()
pygame.key.set_repeat(0,0)

screen = pygame.display.set_mode((TILE_SIZE*(length+2), TILE_SIZE * height))
clock = pygame.time.Clock()