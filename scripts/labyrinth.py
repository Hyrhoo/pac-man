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

    def is_colliding(self, x, y, ghost=False):
        """return if the cell coresponding to the given position is a wall or not

        Args:
            x (int): x position in the labyrinth
            y (int): y position in the labyrinth

        Returns:
            bool: True if the cell is a wall, False otherways
        """
        if self.map[y][x] in self.COLLISION:
            if ghost and self.map[y][x] == 18:
                return False
            return True

    def get_nbr_gommes(self, count_type=(1, 2)):
        res = 0
        for i in self.map:
            res += sum([1 for j in i if j in count_type])
        return res
    
    def get_possible_cells(self, x, y):
        around = []
        for new_x, new_y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (x + new_x, y + new_y)

            if 0 <= node_position[0] < WIDTH and 0 <= node_position[1] < HEIGHT and self.is_colliding(*node_position, True): continue

            around.append(node_position)
        #around = filter(lambda x: (0 <= x[0] < WIDTH and 0 <= x[1] < HEIGHT) and not self.is_colliding(*x, True), around)
        return around
    
    def astar(self, start, end):
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

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
            children = [Node(current_node, i) for i in self.get_possible_cells(*current_node.position)]
            
            # récupération des bons noeux
            for child in children:
                if child in closed_list:
                    continue
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        break
                else:
                    open_list.append(child)


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __str__(self):
        return str(self.position)
    
