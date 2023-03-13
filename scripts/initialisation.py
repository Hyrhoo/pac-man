import pygame, random
from scripts.constantes import *

pygame.mixer.pre_init()
pygame.mixer.set_num_channels(1)

pygame.init()
pygame.key.set_repeat(0,0)

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
sounds["eat"]["fruit"] = pygame.mixer.Sound("data/sounds/eat_fruit.wav")
sounds["eat"]["ghost"] = pygame.mixer.Sound("data/sounds/eat_ghost.wav")
sounds["eat"]["gomme"] = (pygame.mixer.Sound("data/sounds/munch_1.wav"), pygame.mixer.Sound("data/sounds/munch_2.wav"))
sounds["siren"] = {}
sounds["siren"]["1"] = pygame.mixer.Sound("data/sounds/siren_1.wav")
sounds["siren"]["2"] = pygame.mixer.Sound("data/sounds/siren_2.wav")
sounds["siren"]["3"] = pygame.mixer.Sound("data/sounds/siren_3.wav")
sounds["siren"]["4"] = pygame.mixer.Sound("data/sounds/siren_4.wav")
sounds["siren"]["5"] = pygame.mixer.Sound("data/sounds/siren_5.wav")
sounds["siren"]["weak"] = pygame.mixer.Sound("data/sounds/power_pellet.wav")
