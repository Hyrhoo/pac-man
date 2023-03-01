import pygame

pygame.init()
screen=pygame.display.set_mode((200,200))

origin1 = (0,0)
separation = 20

# Load the image
img = pygame.image.load("data/pacman.png")

width, height = img.get_width()/2, img.get_height()
origin2 = origin1[0] + width + separation, origin1[1]

# Blit first half
source_area = pygame.Rect((0,0), (width, height))
screen.blit(img, origin1, source_area)

# Blit second half
source_area = pygame.Rect((width,0), (width, height))
screen.blit(img, origin2, source_area)

pygame.display.update()
while True:
    pass