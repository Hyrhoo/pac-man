from scripts.initialisation import *
from scripts.labyrinth import Labyrinth


class Character(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, speed, direction, labyrinth: Labyrinth):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed * SPEED_MULTI
        self.direction = direction
        self.labyrinth = labyrinth
        self.sprites = []
        self.load_sprites()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)
    
    def load_sprites(self):
        pass

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

    def load_sprite(self, sprite):
        self.sprites.append(pygame.transform.scale(pygame.image.load(f"{DATA_DIRECTORY}/{sprite}.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)))

    @staticmethod
    def pos_in_laby(x, y):
        """give the corresponding position in the labyrinth for the givern position

        Args:
            x (int): the x position in pixel
            y (int): the y position in pixel

        Returns:
            int: the corresponding position in the labyrinth
        """
        return (min(x // TILE_SIZE, WIDTH-1), min(y // TILE_SIZE, HEIGHT-1))

    def get_center_pos(self):
        return self.pos_x+(TILE_SIZE//2), self.pos_y+(TILE_SIZE//2)

    def tp(self):
        """telepost the caracter to the opposite side if he is out of the labyrinth"""
        if self.pos_x <= 0:
            self.set_pos(TILE_SIZE*(WIDTH - 1), self.pos_y)
            return
        if self. pos_x >= TILE_SIZE*(WIDTH - 1):
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
