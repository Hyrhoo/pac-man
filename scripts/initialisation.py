import pygame
from scripts.constantes import *

pygame.init()
pygame.key.set_repeat(0,0)

screen = pygame.display.set_mode((TILE_SIZE*(WIDTH+2), TILE_SIZE * HEIGHT))
clock = pygame.time.Clock()