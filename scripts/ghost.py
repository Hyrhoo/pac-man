from scripts.initialisation import *
from scripts.labyrinth import Labyrinth
from scripts.character import Character
import random

class Ghost(Character):
    direction_to_sens = {(-1,0): 0, (1,0): 1, (0,-1): 2, (0,1): 3}
    spawn = (        (12,12),(13,12),(14,12),(15,12)        ,
             (11,13),(12,14),(13,13),(14,13),(15,13),(16,13),
             (11,14),(12,13),(13,14),(14,14),(15,14),(16,14),
             (11,15),(12,15),(13,15),(14,15),(15,15),(16,15))

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, speed=10, direction=(-1,0), time_in_spawn=0, color=(255, 0, 0)) -> None:
        super().__init__(x, y, speed, direction, labyrinth)
        self.current_sens = self.direction_to_sens[self.direction]
        self.current_cell = None
        self.in_spawn = self.get_actual_cell() in self.spawn
        self.can_go_out = False
        self.creat_time = pygame.time.get_ticks()
        self.time_in_spawn = time_in_spawn
        self.is_weaken = False
        self.time_weaken = 0
        for image in self.sprites:
            pygame.PixelArray(image).replace((237, 28, 36, 255), color)

    def __repr__(self):
        return f"{type(self)} - {(self.pos_x, self.pos_y)}, {self.get_actual_cell()}, {self.labyrinth.map[self.get_actual_cell()[1]][self.get_actual_cell()[0]]} - {self.direction} - {self.in_spawn}, {self.can_go_out}, {self.creat_time}, {self.time_in_spawn}"

    def load_sprites(self):
        for direction in ("left", "right", "up", "down", "weaken"):
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
        cells = self.labyrinth.get_possible_cells(*pos, in_spawn=self.can_go_out)

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
        if self.is_weaken:
            self.current_sens = 4
        self.current_sprite += 1
        if self.current_sprite >= NUMBER_IMG_GHOSTS:
            self.current_sprite -= NUMBER_IMG_GHOSTS
        self.image = self.sprites[int(self.current_sprite + self.current_sens*NUMBER_IMG_GHOSTS)]
    
    def update(self, player) -> None:
        print(self)
        self.animation()
        # gestion déplacement
        actual_cell = self.get_actual_cell()
        if self.current_cell != actual_cell and self.labyrinth.is_intersect(*actual_cell):
            self.current_cell = actual_cell
            possible_move = self.get_possible_cells()
            best_move = self.seek(player)[1]
            tile = self.next_tile_to_take(possible_move, best_move)
            direction = self.direction_to_take(*tile)
            self.change_direction(direction)
        self.move(self.in_spawn)
        
        # spawn gestion
        if self.in_spawn:
            if self.creat_time + self.time_in_spawn <= pygame.time.get_ticks():
                self.can_go_out = True
            if self.get_actual_cell() not in self.spawn:
                self.in_spawn = False
                self.can_go_out = False
                self.direction = (-1, 0)
            
        if self.is_weaken:
            if pygame.time.get_ticks() >= self.time_weaken:
                self.is_weaken = False
                self.current_sens = self.direction_to_sens[self.direction]
    
    def seek(self, player:Character):
        pos = self.get_actual_cell()
        return self.labyrinth.astar(self.pos_in_laby(*self.get_center_pos()), player.pos_in_laby(*player.get_center_pos()), [self.labyrinth.normalize_pos(pos[0]-self.direction[0], pos[1]-self.direction[1])], self.in_spawn)
    
    def weaken(self, time):
        self.is_weaken = True
        self.time_weaken = pygame.time.get_ticks() + time


class Blinky(Ghost):

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, speed=8.7, direction=(-1,0), time_in_spawn=0) -> None:
        super().__init__(labyrinth, x, y, speed, direction, time_in_spawn, (255, 0, 0))


class Pinky(Ghost):

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, speed=8.7, direction=(-1,0), time_in_spawn=3333) -> None:
        super().__init__(labyrinth, x, y, speed, direction, time_in_spawn, (255, 184, 255))


class Inky(Ghost):

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, speed=8.7, direction=(-1,0), time_in_spawn=6666) -> None:
        super().__init__(labyrinth, x, y, speed, direction, time_in_spawn, (0, 255, 255))


   
class Clyde(Ghost):

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, speed=8.7, direction=(-1,0), time_in_spawn=9999) -> None:
        super().__init__(labyrinth, x, y, speed, direction, time_in_spawn, (255, 184, 81))
