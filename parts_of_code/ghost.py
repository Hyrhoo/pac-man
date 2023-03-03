import pygame

from parts_of_code.initialisation import *
from parts_of_code.labyrinth import Labyrinth
from parts_of_code.character import Character

class Ghost(Character):
    direction_to_sens = {(-1,0): 0, (1,0): 1, (0,-1): 2, (0,1): 3}
    base_path = "data/ghost"
    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, anim_len=7, direction=(-1,0), color=(255, 0, 0)) -> None:

        super().__init__(x, y, speed, direction, labyrinth)
        self.anim_len = anim_len
        self.current_sens = self.direction_to_sens[self.direction]
        for image in self.sprites:
            pygame.PixelArray(image).replace((237, 28, 36, 255), color)

        # if self.can_move((self.pos_x+self.direction[0]*TILE_SIZE, self.pos_y+self.direction[1]*TILE_SIZE)):
        #     return
        # can be useful to forbid to the ghosts to go back while moving

    def load_sprites(self):
        for direction in ("left", "right", "up", "down"):
            for index_ in range(1, 8):
                self.load_sprite(f"ghost/{direction}/{index_}")

    def draw_ghost(self):
        """draw the caracter on the screen"""
        screen.blit(self.image, (self.pos_x, self.pos_y))
    
    def update(self) -> None:
        self.current_sprite += 0.5
        if self.current_sprite >= self.anim_len:
            self.current_sprite -= self.anim_len
        self.image = self.sprites[int(self.current_sprite + self.current_sens*self.anim_len)]


class Blinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, anim_len, direction, (255, 0, 0))


class Pinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, anim_len, direction, (255, 184, 255))


class Inky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, anim_len, direction, (0, 255, 255))


   
class Clyde(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, anim_len, direction, (255, 184, 81))