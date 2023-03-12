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
        pygame.draw.line(self.screen, (255, 255, 255), (WIDTH * TILE_SIZE, 0), (WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE))

    def is_colliding(self, x, y, in_spawn=False):
        """return if the cell coresponding to the given position is a wall or not
        Args:
            x (int): x position in the labyrinth
            y (int): y position in the labyrinth
        Returns:
            bool: True if the cell is a wall, False otherways
        """
        if self.map[y][x] in self.COLLISION:
            if in_spawn and self.map[y][x] == 18:
                return False
            return True

    def get_nbr_gommes(self, count_type=(1, 2)):
        """compte le nombre de gommes restante dans le labyrinthe

        Args:
            count_type (tuple[int], optional): le type des gommes à compter. Defaults to (1, 2).

        Returns:
            int: le nombre de gommes comptées
        """
        res = 0
        for i in self.map:
            res += sum([1 for j in i if j in count_type])
        return res
    
    def get_possible_cells(self, x, y, aditiv_wall=[], in_spawn=False):
        """donne les casse valides autoures de la casse donner

        Args:
            x (int): la position x de la case dans le labyrinthe
            y (int): la position y de la case dans le labyrinthe
            aditiv_wall (list[tuple[int]], optional): potientielle mures à rajouter. Defaults to [].
            in_spawn (bool, optional): est-ce que les mures du spawn sont compté. Defaults to False.

        Returns:
            tuple[tuple[int]]: positions valides
        """
        around = []
        for new_x, new_y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (x + new_x, y + new_y)
            around.append(node_position)
        around = map(lambda x: self.normalize_pos(*x), around)
        around = tuple(around)
        around = filter(lambda x: not self.is_colliding(*x, in_spawn) and x not in aditiv_wall, around)
        return tuple(around)
    
    def astar(self, start, end, aditiv_wall=[], in_spawn=False):
        """algorithme A*

        Args:
            start (tuple[int]): la position de la case de départ
            end (tuple[int]): la position de la case d'arriver
            aditiv_wall (list[tuple[int]], optional): mure à rajouté. ils serons effacer après le 1er déplacement calculer. Defaults to [].
            in_spawn (bool, optional): le passage peut-il passer par le spawn ? Defaults to False.

        Raises:
            ValueError: si le chemain n'est pas trouver

        Returns:
            list[tuple[int]]: liste de position qui constitue le chemain à prendre
        """
        if start == end:
            return [start, start]
        start_node = Node(None, start)
        start_node.g = 0
        start_node.h = start_node.f = float("inf")
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        closest = start_node

        open_list = []
        closed_list = []
        open_list.append(start_node)

        while open_list:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            
            open_list.pop(current_index)
            closed_list.append(current_node)

            # fin
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]
            
            # génération des noeux des cases adjacentes
            children = [Node(current_node, i) for i in self.get_possible_cells(*current_node.position, aditiv_wall, in_spawn)]
            aditiv_wall = []
            
            # récupération des bons noeux
            for child in children:
                if child in closed_list:
                    continue
                child.g = current_node.g + 1
                child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))**0.5
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        break
                else:
                    # pour trouver un chemain sans avoir à parcourrir toute la map si le chemain n'existe pas
                    # pour éviter les problème de performance
                    if child.h < closest.h:
                        closest = child
                    elif child.h > closest.h + 10:
                        # après teste, 27 permet de trouver le chemain pour allez d'un coint à l'autre de la map (donc +/- n'importe quelle chemains)
                        # un nombre moins grand (comme 10) devrais quand même permetre aux fantômes de trouver la dirrection pour allez
                        # vers pac-man mais pas le chemain complet (et je suis même pas sûr de ce que je dis)
                        path = []
                        current = closest
                        while current is not None:
                            path.append(current.position)
                            current = current.parent
                        return path[::-1]
                    open_list.append(child)
        
        raise ValueError(f"start point '{start}' has no path to end point '{end}'")   # pour faire une erreur si le chemain n'existe pas
    
    def change_tile(self, x, y, tile):
        """change une luile du labyrinthe

        Args:
            x (int): position x de la tuile dans le labyrinthe
            y (int): position y de la tuile dans le labyrinthe
            tile (int): le numéro correspondant à la nouvelle tuile
        """
        self.map[y][x] = tile
    
    def is_intersect(self, x, y):
        """donne si la position donner est une intersection ou non

        Args:
            x (int): position x de la case dans le labyrinthe
            y (int): position y de la case dans le labyronthe

        Returns:
            bool: True si la position est une intesection. sinon False
        """
        tab = [False, False]
        if not self.is_colliding(*self.normalize_pos(x+1, y)) or not self.is_colliding(*self.normalize_pos(x-1, y)):
            tab[0] = True
        if not self.is_colliding(*self.normalize_pos(x, y+1)) or not self.is_colliding(*self.normalize_pos(x, y-1)):
            tab[1] = True
        return all(tab)
    
    @staticmethod
    def normalize_pos(x, y):
        """normalise la positon donner pour qu'elle soit comprise dans le labyrinthe

        Args:
            x (int): position x à normaliser
            y (int): position y à normaliser

        Returns:
            tuple[int]: la nouvelle positon normaliser
        """
        if x >= WIDTH:
            x = 0
        if x < 0:
            x = WIDTH-1
        return (x, y)


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __repr__(self):
        return f"{self.position}"

    def __eq__(self, other):
        return self.position == other.position
    
    def __str__(self):
        return str(self.position)
    