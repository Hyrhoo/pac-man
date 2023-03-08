from scripts.initialisation import *
from scripts.labyrinth import Labyrinth
from scripts.character import Character
import random

class Ghost(Character):
    direction_to_sens = {(-1,0): 0, (1,0): 1, (0,-1): 2, (0,1): 3}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, direction=(-1,0), color=(255, 0, 0)) -> None:

        super().__init__(x, y, speed, direction, labyrinth)
        self.current_sens = self.direction_to_sens[self.direction]
        self.current_cell = None
        for image in self.sprites:
            pygame.PixelArray(image).replace((237, 28, 36, 255), color)

        # if self.can_move((self.pos_x+self.direction[0]*TILE_SIZE, self.pos_y+self.direction[1]*TILE_SIZE)):
        #     return
        # can be useful to forbid to the ghosts to go back while moving

    def load_sprites(self):
        for direction in ("left", "right", "up", "down"):
            for nbr_img in range(1, NUMBER_IMG_GHOSTS+1):
                self.load_sprite(f"ghost/{direction}/{nbr_img}")
    
    def change_direction(self, new_direction):
        self.direction = new_direction
        self.current_sens = self.direction_to_sens[self.direction]
        pos = self.pos_in_laby(*self.get_front_pos(self.pos_x, self.pos_y, self.direction))
        self.reset_direction(pos)
    
    def get_possible_cells(self):
        def fonc(x):
            if x[0] == pos[0] + self.direction[0] and x[1] == pos[1] + self.direction[1]:
                return True
            if self.direction[1] and x[0] == pos[0]:
                return False
            if self.direction[0] and x[1] == pos[1]:
                return False
            return True
        
        pos = self.get_actual_cell()
        cells = self.labyrinth.get_possible_cells(*pos)

        return tuple(filter(fonc, cells))
    
    def direction_to_take(self, x, y):
        g_x, g_y = self.get_actual_cell()
        if g_x < x:
            return (1, 0)
        if g_x > x:
            return (-1, 0)
        if g_y < y:
            return (0, 1)
        if g_y > y:
            return (0, -1)
        return self.direction

    def next_tile_to_take(self, possible_move, best_move):
        next_move = random.choice(possible_move)
        if best_move in possible_move:
            next_move = best_move
        return next_move

    def animation(self):
        self.current_sprite += 1
        if self.current_sprite >= NUMBER_IMG_GHOSTS:
            self.current_sprite -= NUMBER_IMG_GHOSTS
        self.image = self.sprites[int(self.current_sprite + self.current_sens*NUMBER_IMG_GHOSTS)]
    
    def update(self, player) -> None:
        self.animation()
        actual_cell = self.get_actual_cell()
        if self.current_cell != actual_cell and self.labyrinth.is_intersect(*actual_cell):
            self.current_cell = actual_cell
            possible_move = self.get_possible_cells()
            best_move = self.seek(player)[1]
            tile = self.next_tile_to_take(possible_move, best_move)
            direction = self.direction_to_take(*tile)
            self.change_direction(direction)
        have_move = self.move(True)
    
    def seek(self, player:Character):
        pos = self.get_actual_cell()
        return self.labyrinth.astar(self.pos_in_laby(*self.get_center_pos()), player.pos_in_laby(*player.get_center_pos()), [self.labyrinth.normalize_pos(pos[0]-self.direction[0], pos[1]-self.direction[1])])


class Blinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, direction, (255, 0, 0))


class Pinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, direction, (255, 184, 255))


class Inky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, direction, (0, 255, 255))


   
class Clyde(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, direction, (255, 184, 81))
