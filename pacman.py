import pygame

    # ==== variables ==== #

GLOBAL_FPS = 60     # FPS global du jeu
TILE_SIZE = 32      # definition du dessin (carré)
length = 28         # hauteur du niveau
height = 31         # largeur du niveau
tiles = []          # liste d'images tiles

    # ==== classes ==== #

class Labyrinth:
    
    def __init__(self, file):
        self.map = load_map(file)
    
    def drawlevel(self):
        """
        affiche le niveau a partir de la liste a deux dimensions niveau[][]
        """
        for y, ligne in enumerate(self.map):
            for x, case in enumerate(ligne):
                screen.blit(tiles[case], (x * TILE_SIZE, y * TILE_SIZE))
        pygame.draw.line(screen, "#FFFFFF", (length * TILE_SIZE, 0), (length * TILE_SIZE, height * TILE_SIZE))

class Pac_man:
    pass

class Ghost:
    pass

    # ==== fonctions ==== #

def loadtile(file):
   img = pygame.image.load(file).convert()
   return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))


def load_map(file):
    with open(file, "r") as f:
        labyrinth = []
        for line in f.readlines():
            labyrinth.append([int(i) for i in line.strip("\n").split()])
        return labyrinth

    # ==== init ==== #

pygame.init()
screen = pygame.display.set_mode((TILE_SIZE * (length + 10), TILE_SIZE * height))
clock = pygame.time.Clock()

for n in range(18):
    tiles.append(loadtile(f"data/{n}.png"))
img_pacman = loadtile("data/pacman.png")
imp_ghost = loadtile("data/ghost.png")

labyrinth = Labyrinth("map.txt")

    # ==== main loop ==== #

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    labyrinth.drawlevel()
    pygame.display.flip()
    print(clock.get_fps())  # juste pour afficher les fps
    clock.tick(GLOBAL_FPS)

pygame.quit()