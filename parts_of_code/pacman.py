import pygame

from parts_of_code.labyrinth import Labyrinth
from parts_of_code.character import Character


class Pac_man(Character):
    keys_directions = {pygame.K_UP: (0,-1), pygame.K_DOWN: (0,1), pygame.K_LEFT: (-1,0), pygame.K_RIGHT: (1,0)}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, direction=(1,0)) -> None:

        super().__init__(x, y, speed, direction, labyrinth)
        self.input_direction = None

    def load_sprites(self):
        for index_ in range(1, 6):
            self.load_sprite(f"pacman/{index_}")

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
