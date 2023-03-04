from scripts.initialisation import *

class Labyrinth:
    COLLISION = range(3, 19)

    def __init__(self, map_file, screen):
        """initialise les données de la classe en chargeant d'abord les images puis les datas de la map


        Args:
            map_file (str): le nom du fichier à charger
        """
        self.screen = screen
        self.load_tiles()
        self.load_map(map_file)

    def load_tiles(self):
        """charge les images nécessaires à l'affichage du labyrinthe"""
        self.tiles = []
        for n in range(NUMBRE_IMG):
            self.tiles.append(pygame.transform.scale(pygame.image.load(f"{DATA_DIRECTORY}/tiles/{n}.png").convert(), (TILE_SIZE, TILE_SIZE)))

    def load_map(self, file):
        """charge le fichier contenant les datas de la map

        Args:
            file (str): le nom du fichier à charger
        """
        with open(file, "r") as f:
            self.map = []
            for line in f.readlines():
                self.map.append([int(i) for i in line.strip("\n").split()])

    def draw_level(self):
        """affiche le niveau a partir de la liste a deux dimensions self.map[][]"""
        for y, ligne in enumerate(self.map):
            for x, case in enumerate(ligne):
                self.screen.blit(self.tiles[case], (x * TILE_SIZE, y * TILE_SIZE))
        pygame.draw.line(self.screen, (255, 255, 255), (length * TILE_SIZE, 0), (length * TILE_SIZE, height * TILE_SIZE))

    def is_colliding(self, x, y):
        """return if the cell coresponding to the given position is a wall or not

        Args:
            x (int): x position in the labyrinth
            y (int): y position in the labyrinth

        Returns:
            bool: True if the cell is a wall, False otherways
        """
        return self.map[y][x] in self.COLLISION

    def get_nbr_gommes(self, count_type=(1, 2)):
        res = 0
        for i in self.map:
            res += sum([1 for j in i if j in count_type])
        return res