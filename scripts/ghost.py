from scripts.initialisation import *
from scripts.labyrinth import Labyrinth
from scripts.character import Character

class Ghost(Character):
    direction_to_sens = {(-1,0): 0, (1,0): 1, (0,-1): 2, (0,1): 3}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, direction=(-1,0), color=(255, 0, 0)) -> None:

        super().__init__(x, y, speed, direction, labyrinth)
        self.current_sens = self.direction_to_sens[self.direction]
        for image in self.sprites:
            pygame.PixelArray(image).replace((237, 28, 36, 255), color)

        # if self.can_move((self.pos_x+self.direction[0]*TILE_SIZE, self.pos_y+self.direction[1]*TILE_SIZE)):
        #     return
        # can be useful to forbid to the ghosts to go back while moving

    def load_sprites(self):
        for direction in ("left", "right", "up", "down"):
            for nbr_img in range(1, NUMBER_IMG_GHOSTS+1):
                self.load_sprite(f"ghost/{direction}/{nbr_img}")
    
    def update(self) -> None:
        self.current_sprite += 1
        if self.current_sprite >= NUMBER_IMG_GHOSTS:
            self.current_sprite -= NUMBER_IMG_GHOSTS
        self.image = self.sprites[int(self.current_sprite + self.current_sens*NUMBER_IMG_GHOSTS)]


class Blinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, direction, (255, 0, 0))


class Pinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, direction, (255, 184, 255))


class Inky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, direction, (0, 255, 255))


   
class Clyde(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, direction, (255, 184, 81))