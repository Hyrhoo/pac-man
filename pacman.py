import pygame

    # ==== variables ==== #

GLOBAL_FPS = 60     # FPS global du jeu
TILE_SIZE = 32      # definition du dessin (carré)
length = 28         # hauteur du niveau
height = 31         # largeur du niveau
tiles = []          # liste d'images tiles

    # ==== classes ==== #

class Labyrinth:
    pass

class Pac_man:
    pass

class Ghost:
    pass

    # ==== fonctions ==== #

def loadtile(file):
   return pygame.transform.scale(pygame.image.load(file), (TILE_SIZE, TILE_SIZE))

def drawlevel(niveau):
    """
    affiche le niveau a partir de la liste a deux dimensions niveau[][]
    """
    for y in range(height):
        for x in range(length):
            screen.blit(tiles[niveau[y][x]], (x * TILE_SIZE, y * TILE_SIZE))
    pygame.draw.line(screen, "#FFFFFF", (length * TILE_SIZE, 0), (length * TILE_SIZE, height * TILE_SIZE))

def load_map(file):
    with open(file, "r") as f:
        labyrinth = []
        for line in f.readlines():
            labyrinth.append([int(i) for i in line.strip("\n").split()])
        return labyrinth

    # ==== init ==== #

for n in range(18):
    tiles.append(loadtile(f"data/{n}.png"))
img_pacman = loadtile("data/pacman.png")
imp_ghost = loadtile("data/ghost.png")
map = load_map("map.txt")

screen = pygame.display.set_mode((TILE_SIZE * (length + 10), TILE_SIZE * height))
clock = pygame.time.Clock()

    # ==== main loop ==== #

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    drawlevel(map)
    pygame.display.flip()
    clock.tick(GLOBAL_FPS)

pygame.quit()