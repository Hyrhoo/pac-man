import pygame

    # ==== variables ==== #

GLOBAL_FPS = 60     # FPS global du jeu
TILE_SIZE = 32      # definition du dessin (carré)
NUMBRE_IMG = 18     # nombre d'images à charger
length = 28         # hauteur du niveau
height = 31         # largeur du niveau

    # ==== classes ==== #

class Labyrinth:
    
    def __init__(self, map_file):
        """
        initialise les données de la classe en chargeant d'abord les images puis les datas de la map

        Args:
            map_file (str): le nom du fichier à charger
        """
        self.load_tiles()
        self.load_map(map_file)

    def load_tiles(self):
        """
        charge les images nécessaires à l'affichage du labyrinthe
        """
        self.tiles = []
        for n in range(NUMBRE_IMG):
            self.tiles.append(pygame.transform.scale(pygame.image.load(f"data/{n}.png").convert(), (TILE_SIZE, TILE_SIZE)))
    
    def load_map(self, file):
        """
        charge le fichier contenant les datas de la map

        Args:
            file (str): le nom du fichier à charger
        """
        with open(file, "r") as f:
            labyrinth = []
            for line in f.readlines():
                labyrinth.append([int(i) for i in line.strip("\n").split()])
        self.map = labyrinth
    
    def drawlevel(self):
        """
        affiche le niveau a partir de la liste a deux dimensions self.map[][]
        """
        for y, ligne in enumerate(self.map):
            for x, case in enumerate(ligne):
                screen.blit(self.tiles[case], (x * TILE_SIZE, y * TILE_SIZE))
        pygame.draw.line(screen, "#FFFFFF", (length * TILE_SIZE, 0), (length * TILE_SIZE, height * TILE_SIZE))


class Pac_man:
    
    def __init__(self) -> None:
        self.img = pygame.transform.scale(pygame.image.load("data/pacman.png").convert(), (TILE_SIZE, TILE_SIZE))


class Ghost:
    
    def __init__(self) -> None:
        self.img = pygame.transform.scale(pygame.image.load("data/ghost.png").convert(), (TILE_SIZE, TILE_SIZE))

    # ==== fonctions ==== #



    # ==== init ==== #

pygame.init()
screen = pygame.display.set_mode((TILE_SIZE * (length + 10), TILE_SIZE * height))
clock = pygame.time.Clock()

labyrinth = Labyrinth("map.txt")
player = Pac_man()
ghost = Ghost()

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