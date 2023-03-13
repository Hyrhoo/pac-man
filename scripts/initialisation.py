import pygame, random
from scripts.constantes import *

pygame.mixer.pre_init()

pygame.init()
pygame.key.set_repeat(0,0)
pygame.mixer.set_num_channels(3)

screen = pygame.display.set_mode((TILE_SIZE*(WIDTH+2), TILE_SIZE * HEIGHT))
clock = pygame.time.Clock()

sounds = {}
sounds["off game"] = {}
sounds["off game"]["start"] = pygame.mixer.Sound("data/sounds/game_start.wav")
sounds["off game"]["end"] = pygame.mixer.Sound("data/sounds/intermission.wav")
sounds["death"] = {}
sounds["death"]["1"] = pygame.mixer.Sound("data/sounds/death_1.wav")
sounds["death"]["2"] = pygame.mixer.Sound("data/sounds/death_2.wav")
sounds["eat"] = {}
sounds["eat"]["ghost"] = pygame.mixer.Sound("data/sounds/eat_ghost.wav")
sounds["eat"]["gomme"] = (pygame.mixer.Sound("data/sounds/munch_1.wav"), pygame.mixer.Sound("data/sounds/munch_2.wav"))
sounds["siren"] = {}
sounds["siren"]["1"] = pygame.mixer.Sound("data/sounds/siren_1.wav")
sounds["siren"]["weak"] = pygame.mixer.Sound("data/sounds/power_pellet.wav")
