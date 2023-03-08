from scripts.initialisation import *
from scripts.labyrinth import Labyrinth
from scripts.character import Character

class Ghost(Character):
    direction_to_sens = {(-1,0): 0, (1,0): 1, (0,-1): 2, (0,1): 3}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, direction=(-1,0), color=(255, 0, 0)) -> None:

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
    
    def change_direction(self, new_direction):
        self.direction = new_direction
        self.current_sens = self.direction_to_sens[self.direction]
        pos = self.pos_in_laby(*self.get_front_pos(self.pos_x, self.pos_y, self.direction))
        self.reset_direction(pos)
    
    def get_possible_cells(self):
        pos = self.get_actual_cell()
        cells = self.labyrinth.get_possible_cells(*pos)
        print(cells)
        def fonc(x):
            if x[0] == pos[0] + self.direction[0] and x[1] == pos[1] + self.direction[1]:
                return True
            if self.direction[1] and x[0] != pos[0]:
                return False
            if self.direction[0] and x[1] != pos[1]:
                return False
            return True
        
        return tuple(filter(fonc, cells))
    
    def directuion_to_take(self, x, y):
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

    def next_tile_to_take(self, possible_move, path):
        next_move = possible_move[0]
        for v in possible_move:
            if v in path:
                if next_move not in path:
                    next_move = v
                else:
                    if path.index(v) < path.index(next_move):
                        next_move = v
        return next_move

    def animation(self):
        self.current_sprite += 1
        if self.current_sprite >= NUMBER_IMG_GHOSTS:
            self.current_sprite -= NUMBER_IMG_GHOSTS
        self.image = self.sprites[int(self.current_sprite + self.current_sens*NUMBER_IMG_GHOSTS)]
    
    def update(self, player) -> None:
        self.animation()
        possible_move = self.get_possible_cells()
        print(possible_move, self.get_actual_cell(), self.direction)
        if len(possible_move) > 1:   # can change direction
            path = self.chasse(player)
            tile = self.next_tile_to_take(possible_move, path)
            direction = self.directuion_to_take(*tile)
            self.change_direction(direction)
        elif possible_move[0] != (self.pos_x + self.direction[0], self.pos_y + self.direction[1]):
            direction = self.directuion_to_take(*possible_move[0])
            self.change_direction(direction)
        have_move = self.move(True)
    
    def chasse(self, player:Character):
        return self.labyrinth.astar(self.pos_in_laby(*self.get_center_pos()), player.pos_in_laby(*player.get_center_pos()))


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