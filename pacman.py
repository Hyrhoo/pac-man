import pygame
from time import monotonic

    # ==== variables ==== #

GLOBAL_FPS = 30     # FPS global du jeu
TILE_SIZE = 32      # definition du dessin (carré)
NUMBRE_IMG = 19     # nombre d'images à charger
length = 28         # hauteur du niveau
height = 31         # largeur du niveau
SPEED_MULTI = TILE_SIZE/50

    # ==== classes ==== #

class Labyrinth:
    COLLISION = range(3, 19)

    def __init__(self, map_file):
        """initialise les données de la classe en chargeant d'abord les images puis les datas de la map


        Args:
            map_file (str): le nom du fichier à charger
        """
        self.load_tiles()
        self.load_map(map_file)

    def load_tiles(self):
        """charge les images nécessaires à l'affichage du labyrinthe"""
        self.tiles = []
        for n in range(NUMBRE_IMG):
            self.tiles.append(pygame.transform.scale(pygame.image.load(f"data/{n}.png").convert(), (TILE_SIZE, TILE_SIZE)))

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
                screen.blit(self.tiles[case], (x * TILE_SIZE, y * TILE_SIZE))
        pygame.draw.line(screen, (255, 255, 255), (length * TILE_SIZE, 0), (length * TILE_SIZE, height * TILE_SIZE))

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


class Character(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, speed, direction, image_paths, labyrinth: Labyrinth):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed * SPEED_MULTI
        self.direction = direction
        self.labyrinth = labyrinth
        self.sprites = []
        self.load_sprires(image_paths)
        #for image_path in image_paths:
        #    self.sprites.append(pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (TILE_SIZE, TILE_SIZE)))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)

    def load_sprires(self, sprites):
        for sprite in sprites:
            self.sprites.append(pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), (TILE_SIZE, TILE_SIZE)))

    def set_pos(self, x, y):
        """set the caracter at the given position

        Args:
            x (int): the x position of the caracter
            y (int): the y position of the caracter
        """
        self.pos_x, self.pos_y = x, y
        self.rect.topleft = (x, y)

    @staticmethod
    def get_front_pos(x, y, direction):
        """get the position of the pixel on the front of the caracter at the given position

        Args:
            x (int): the x position of the caracter
            y (int): the y position of the caracter
            direction (tuple[int]): the direction of the caracter

        Returns:
            tuple[int]: the position of the pixel on the middle of the side at the direction of the caracter
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
        """give the corresponding position in the labyrinth for the givern position

        Args:
            x (int): the x position in pixel
            y (int): the y position in pixel

        Returns:
            int: the corresponding position in the labyrinth
        """
        return (min(x // TILE_SIZE, length-1), min(y // TILE_SIZE, height-1))

    def get_center_pos(self):
        return self.pos_x+(TILE_SIZE//2), self.pos_y+(TILE_SIZE//2)

    def tp(self):
        """telepost the caracter to the opposite side if he is out of the labyrinth"""
        if self.pos_x <= 0:
            self.set_pos(TILE_SIZE*(length - 1), self.pos_y)
            return
        if self. pos_x >= TILE_SIZE*(length - 1):
            self.set_pos(0, self.pos_y)
            return
        
    def can_move(self, new_pos):
        """Check if the caracter can move"""
        front_pos = self.get_front_pos(*new_pos, self.direction)
        pos_in_laby = self.pos_in_laby(*front_pos)
        return not self.labyrinth.is_colliding(*pos_in_laby)


    def move(self):
        """move the caracter from his direction and his speed"""
        new_pos = (self.pos_x + round(self.direction[0]*self.speed), self.pos_y + round(self.direction[1]*self.speed))
        if not self.can_move(new_pos):
            self.correction_pos()
            return False
        self.set_pos(*new_pos)
        self.tp()
        return True

    def correction_pos(self):
        pos_in_laby = self.pos_in_laby(*self.get_center_pos())
        self.set_pos(pos_in_laby[0]*TILE_SIZE, pos_in_laby[1]*TILE_SIZE)
    
    def reset_direction(self, pos_in_laby):
        """reset the position of the caracter when he change direction so that he stays in the middle of its row / column

        Args:
            pos_in_laby (tuple[int]): the actual pos in the labyrinth of the caracter
        """
        if self.direction[0]:
            self.set_pos(self.pos_x, TILE_SIZE * pos_in_laby[1])
        if self.direction[1]:
            self.set_pos(TILE_SIZE * pos_in_laby[0], self.pos_y)


class Pac_man(Character):
    keys_directions = {pygame.K_UP: (0,-1), pygame.K_DOWN: (0,1), pygame.K_LEFT: (-1,0), pygame.K_RIGHT: (1,0)}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, image_paths=["data/pacman_1.png", "data/pacman_2.png", "data/pacman_3.png", "data/pacman_4.png", "data/pacman_5.png", "data/pacman_4.png", "data/pacman_3.png", "data/pacman_2.png"], direction=(1,0)) -> None:
        super().__init__(x, y, speed, direction, image_paths, labyrinth)
        self.input_direction = None

    def get_input_direction(self, keys):
        """get the direction enter by the player

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
        """change the direction of the player if he has enter one and the caracter can change direction"""
        if self.input_direction is not None:
            front_pos = self.get_front_pos(self.pos_x, self.pos_y, self.input_direction)
            pos_in_laby = self.pos_in_laby(*front_pos)
            if self.labyrinth.is_colliding(*pos_in_laby):
                return
            self.direction = self.input_direction
            pos_in_laby = self.pos_in_laby(*front_pos)
            self.reset_direction(pos_in_laby)
            self.input_direction = None

    def update(self, keys):
        """call all the required fonction for the update of the caracter each frame 

        Args:
            keys (tuple[Pygame Event]): the event enter this frame
        """
        self.get_input_direction(keys)
        self.set_direction()
        have_move = self.move()
        if have_move:
            self.animate()

    def animate(self):
        """draw the caracter on the screen"""
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite -= len(self.sprites)
        # allow to not turn the base image
        self.image = self.sprites[int(self.current_sprite)].copy()
        # allow to turn the image
        if self.direction == (0, -1):
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == (0, 1):
            self.image = pygame.transform.rotate(self.image, 90)
            self.image = pygame.transform.flip(self.image, False, True)
        elif self.direction == (-1, 0):
            self.image = pygame.transform.flip(self.image, True, False)


class Ghost(Character):
    direction_to_sens = {(-1,0): 0, (1,0): 1, (0,-1): 2, (0,1): 3}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png"],
                 anim_len=7, direction=(-1,0), color=(255, 0, 0)) -> None:
        super().__init__(x, y, speed, direction, image_paths, labyrinth)
        self.anim_len = anim_len
        self.current_sens = self.direction_to_sens[self.direction]
        for image in self.sprites:
            pygame.PixelArray(image).replace((237, 28, 36, 255), color)

        # if self.can_move((self.pos_x+self.direction[0]*TILE_SIZE, self.pos_y+self.direction[1]*TILE_SIZE)):
        #     return
        # can be useful to forbid to the ghosts to go back while moving

    def draw_ghost(self):
        """draw the caracter on the screen"""
        screen.blit(self.image, (self.pos_x, self.pos_y))
    
    def update(self) -> None:
        self.current_sprite += 1
        if self.current_sprite >= self.anim_len:
            self.current_sprite -= self.anim_len
        self.image = self.sprites[int(self.current_sprite + self.current_sens*self.anim_len)]


class Blinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png"],
                 anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_paths, anim_len, direction, (255, 0, 0))


class Pinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png"],
                 anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_paths, anim_len, direction, (255, 184, 255))


class Inky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png"],
                 anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_paths, anim_len, direction, (0, 255, 255))


   
class Clyde(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png"],
                 anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_paths, anim_len, direction, (255, 184, 81))


    # ==== fonctions ==== #



    # ==== init ==== #

pygame.init()
pygame.key.set_repeat(0,0)
screen = pygame.display.set_mode((TILE_SIZE*(length+2), TILE_SIZE * height))
clock = pygame.time.Clock()

player_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
labyrinth = Labyrinth("map.txt")
player = Pac_man(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*23, labyrinth)

blinky = Blinky(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*11, labyrinth)
pinky = Pinky(TILE_SIZE*11 + TILE_SIZE//2, TILE_SIZE*14, labyrinth)
inky = Inky(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*14, labyrinth)
clyde = Clyde(TILE_SIZE*15 + TILE_SIZE//2, TILE_SIZE*14, labyrinth)

player_group.add(player)
ghost_group.add(blinky)
ghost_group.add(pinky)
ghost_group.add(inky)
ghost_group.add(clyde)

    # ==== main loop ==== #

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
    #player.update(keys)
    player_group.update(keys)
    player_group.draw(screen)
    ghost_group.update()
    ghost_group.draw(screen)
    
    pygame.display.flip()
    #print(clock.get_fps())  # juste pour afficher les fps
    clock.tick(GLOBAL_FPS)

pygame.quit()
