import pygame
from time import monotonic

    # ==== variables ==== #

GLOBAL_FPS = 30     # FPS global du jeu
TILE_SIZE = 28      # definition du dessin (carré)
NUMBRE_IMG = 19     # nombre d'images à charger
length = 28         # hauteur du niveau
height = 31         # largeur du niveau

    # ==== classes ==== #

class Labyrinth:
    COLLISION = range(3, 19)

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
            self.map = []
            for line in f.readlines():
                self.map.append([int(i) for i in line.strip("\n").split()])

    def draw_level(self):
        """
        affiche le niveau a partir de la liste a deux dimensions self.map[][]
        """
        for y, ligne in enumerate(self.map):
            for x, case in enumerate(ligne):
                screen.blit(self.tiles[case], (x * TILE_SIZE, y * TILE_SIZE))
        pygame.draw.line(screen, "#FFFFFF", (length * TILE_SIZE, 0), (length * TILE_SIZE, height * TILE_SIZE))

    def is_colliding(self, x, y):
        """return if the cell coresponding to the given position is a wall or not

        Args:
            x (int): x position in the labyrinth
            y (int): y position in the labyrinth

        Returns:
            bool: True if the cell is a wall, False otherways
        """
        return self.map[y][x] in self.COLLISION


class Character:

    def __init__(self, pos_x, pos_y, speed, direction, image_path, labyrinth: Labyrinth):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        pygame.PixelArray(self.image).replace((0, 0, 0, 255), (0, 0, 0, 0))
        self.labyrinth = labyrinth

    def draw_character(self):
        """
        draw the caracter on the screen
        """
        screen.blit(self.image, (self.pos_x, self.pos_y))

    @staticmethod
    def get_front_pos(x, y, direction):
        """
        get the position of the pixel on the fronte of the caracter at the given position

        Args:
            x (int): the x potition of the caracter
            y (int): the y position of the caracter
            direction (tuple[int]): the direction of the caracter

        Returns:
            tuple[int]: the positioin of the pixel on the middle of the side at the direction of the caracter
        """
        if direction[0] == 1:
            return (x+TILE_SIZE, y+(TILE_SIZE//2))
        if direction[0] == -1:
            return (x-1, y+(TILE_SIZE//2))
        if direction[1] == 1:
            return (x+(TILE_SIZE//2), y+TILE_SIZE)
        if direction[1] == -1:
            return (x+(TILE_SIZE//2), y-1)

    @staticmethod
    def pos_in_laby(x, y):
        """
        give the corresponding position in the labyrinth for the givern position

        Args:
            x (int): the x position in pixel
            y (int): the y position in pixel

        Returns:
            int: the corresponding position in the labyrinth
        """
        return (min(x // TILE_SIZE, length-1), min(y // TILE_SIZE, height-1))

    def tp(self):
        """
        telepost the caracter to the opposite side if he is out of the labyrinth
        """
        if self.pos_x <= 0:
            self.pos_x = TILE_SIZE*(length - 1)
            return
        if self. pos_x >= TILE_SIZE*(length - 1):
            self.pos_x = 0
            return

    def move(self):
        """
        move the caracter from his direction and his speed
        """
        new_pos = (self.pos_x + self.direction[0]*self.speed, self.pos_y + self.direction[1]*self.speed)
        front_pos = self.get_front_pos(*new_pos, self.direction)
        pos_in_laby = self.pos_in_laby(*front_pos)
        if self.labyrinth.is_colliding(*pos_in_laby):
            return
        self.pos_x, self.pos_y = new_pos
        self.tp()

    def reset_direction(self, pos_in_laby):
        """
        reset the position of the caracter when he change direction so that he stays in the middle of its row / column

        Args:
            pos_in_laby (tuple[int]): the actual pos in the labyrinth of the caracter
        """
        if self.direction[0]:
            self.pos_y = TILE_SIZE * pos_in_laby[1]
        if self.direction[1]:
            self.pos_x = TILE_SIZE * pos_in_laby[0]


class Pac_man(Character):

    keys_directions = {pygame.K_UP: (0,-1), pygame.K_DOWN: (0,1), pygame.K_LEFT: (-1,0), pygame.K_RIGHT: (1,0)}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=7, image_path="data/pacman.png", direction=(1,0)) -> None:
        Character.__init__(self, x, y, speed, direction, image_path, labyrinth)
        self.input_direction = None

    def get_input_direction(self, keys):
        """
        get the direction enter by the player

        Args:
            keys (tuple[Pygame Event]): the event enter this frame
        """
        keys = [key.key for key in keys if key.type == pygame.KEYDOWN] # avoir que les input KEYDOWN
        for key in keys:
            if key in self.keys_directions:
                value = self.keys_directions[key]
                if value != self.direction:
                    self.input_direction = value

    def set_direction(self):
        """
        change the direction of the player if he has enter one and the caracter can change direction
        """
        if self.input_direction is not None:
            front_pos = self.get_front_pos(self.pos_x, self.pos_y, self.input_direction)
            pos_in_laby = self.pos_in_laby(*front_pos)
            if self.labyrinth.is_colliding(*pos_in_laby):
                return
            self.direction = self.input_direction
            self.reset_direction(pos_in_laby)
            self.input_direction = None

    def update(self, keys):
        """
        call all the required fonction for the update of the caracter each frame 

        Args:
            keys (tuple[Pygame Event]): the event enter this frame
        """
        self.get_input_direction(keys)
        self.set_direction()
        self.move()
        self.draw_character()


class Ghost(Character):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, image_path="data/ghost.png", direction=(1,0), color=(255, 0, 0)) -> None:
        Character.__init__(self, x, y, speed, direction, image_path, labyrinth)
        pygame.PixelArray(self.image).replace((237, 28, 36, 255), color)


class Blinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, image_path="data/ghost.png", direction=(1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_path, direction, (255, 0, 0))


class Pinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, image_path="data/ghost.png", direction=(1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_path, direction, (255, 184, 255))


class Inky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, image_path="data/ghost.png", direction=(1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_path, direction, (0, 255, 255))


   
class Clyde(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, image_path="data/ghost.png", direction=(1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_path, direction, (255, 184, 81))


    # ==== fonctions ==== #



    # ==== init ==== #

pygame.init()
screen = pygame.display.set_mode((TILE_SIZE*(length+2), TILE_SIZE * height))
clock = pygame.time.Clock()

labyrinth = Labyrinth("map.txt")
player = Pac_man(TILE_SIZE * 13+TILE_SIZE//2, TILE_SIZE*23, labyrinth)
ghost = Ghost(1,1,labyrinth)

    # ==== main loop ==== #
pygame.key.set_repeat(0,0)
run = True
while run:
    labyrinth.draw_level()
    keys = pygame.event.get()
    for event in keys:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    player.update(keys)
    
    pygame.display.flip()
    #print(clock.get_fps())  # juste pour afficher les fps
    clock.tick(GLOBAL_FPS)

pygame.quit()
