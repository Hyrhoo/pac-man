from scripts.initialisation import *
from scripts.labyrinth import Labyrinth
from scripts.character import Character

from time import monotonic

class Pac_man(Character):
    keys_directions = {pygame.K_UP: (0,-1), pygame.K_DOWN: (0,1), pygame.K_LEFT: (-1,0), pygame.K_RIGHT: (1,0)}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=10, direction=(1,0)) -> None:

        super().__init__(x, y, speed, direction, labyrinth)
        self.input_direction = None
        self.score = 0
        self.slow = False
        self.nb_eat = 0


    def load_sprites(self):
        for nbr_img in range(1, NUMBER_IMG_PACMAN+1):
            self.load_sprite(f"pacman/{nbr_img}")

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

    def update(self, keys, ghost_group):
        """call all the required functions for the update of the caracter each frame 

        Args:
            keys (tuple[Pygame Event]): the event enter this frame
        """
        self.get_input_direction(keys)
        temporary_speed = self.speed
        if self.slow:
            self.speed = 0.6*self.speed
        self.set_direction()
        have_move = self.move()
        if have_move:
            self.animate()
        if self.slow:
            self.speed = temporary_speed
            self.slow = False
        self.eat(ghost_group)
        # check the hitboxes
        #screen.fill("#FF0000",pygame.Rect(self.pos_x, self.pos_y, TILE_SIZE, TILE_SIZE))

    def eat(self, ghost_group):
        """Try to eat everything on his way !"""
        self.eat_pac_gomme(ghost_group)
        self.eat_ghost(ghost_group)
    
    def eat_pac_gomme(self, ghost_group):
        x, y = self.get_actual_cell()
        case = self.labyrinth.map[y][x]
        if case == 1:
            self.score += 10
            self.labyrinth.change_tile(x, y, 0)
            self.slow = True
        elif case == 2:
            self.score += 50
            self.labyrinth.change_tile(x, y, 0)
            for ghost in ghost_group:
                ghost.weaken(10_000)
            self.nb_eat = 0
            self.slow = True


    def eat_ghost(self, ghost_group):
        x, y, width, height = pygame.mask.from_surface(self.image).get_bounding_rects()[0]
        x += self.pos_x
        y += self.pos_y

        for ghost in ghost_group:
            x_ghost, y_ghost, width_ghost, height_ghost = pygame.mask.from_surface(ghost.image).get_bounding_rects()[0]
            x_ghost += ghost.pos_x
            y_ghost += ghost.pos_y
            
            if (x+0.2*width<x_ghost+width_ghost<x+width or x<x_ghost<x+width-0.2*width) and (y<y_ghost+height_ghost<y+height or y<y_ghost<y+height-0.2*height):
                if ghost.is_weaken:
                    ghost_group.remove(ghost)
                    new_ghost = type(ghost)(self.labyrinth, time_in_spawn=random.randint(5000, 8000))
                    ghost_group.add(new_ghost)
                    self.score += 200 * 2 ** self.nb_eat
                    self.nb_eat += 1
                else:
                    import sys
                    print("T'es trop con, t'es mort !")
                    sys.exit()


    def animate(self):
        """draw the caracter on the screen"""
        self.current_sprite += 1
        if self.current_sprite >= NUMBER_IMG_PACMAN:
            self.current_sprite -= NUMBER_IMG_PACMAN
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
