import pygame

pygame.init()
pygame.key.set_repeat(0,0)

GLOBAL_FPS = 30                 # FPS global du jeu
TILE_SIZE = 32                  # definition du dessin (carré)
NUMBRE_IMG = 19                 # nombre d'images à charger
length = 28                     # hauteur du niveau
height = 31                     # largeur du niveau
SPEED_MULTI = TILE_SIZE/50      # pour faire correspondre la vitesse des personages à la tail de la fenêtre

screen = pygame.display.set_mode((TILE_SIZE*(length+2), TILE_SIZE * height))
clock = pygame.time.Clock()