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
        self.is_seeker = False
        self.seek_time = 0


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

    def update(self, keys):
        """call all the required functions for the update of the caracter each frame 

        Args:
            keys (tuple[Pygame Event]): the event enter this frame
        """
        self.get_input_direction(keys)
        self.set_direction()
        have_move = self.move()
        if self.seek_time < monotonic():
            self.is_seeker = False
        if have_move:
            self.animate()
        # check the hitboxes
        #screen.fill("#FF0000",pygame.Rect(self.pos_x, self.pos_y, TILE_SIZE, TILE_SIZE))

    def eat(self, ghost_group):
        """Try to eat everything on his way !"""
        self.eat_pac_gomme()
        self.eat_ghost(ghost_group)
    
    def eat_pac_gomme(self):
        x, y = self.get_actual_cell()
        case = self.labyrinth.map[y][x]
        if case == 1:
            self.score += 10
            self.labyrinth.change_tile(x, y, 0)
        elif case == 2:
            self.score += 50
            self.labyrinth.change_tile(x, y, 0)
            self.seek_time = monotonic() + 10
            self.is_seeker = True
        
    def eat_ghost(self, ghost_group):
        start_self_x, start_self_y = self.pos_x, self.pos_y
        end_self_x, end_self_y = start_self_x + TILE_SIZE, start_self_y + TILE_SIZE
        for ghost in ghost_group:
            start_ghost_x, start_ghost_y = ghost.pos_x, ghost.pos_y
            end_ghost_x, end_ghost_y = start_ghost_x+TILE_SIZE, start_ghost_y+TILE_SIZE
            if ((start_ghost_x <= start_self_x <= end_ghost_x and start_ghost_y <= start_self_y <= end_ghost_y)
            or (start_self_x <= start_ghost_x <= end_self_x and start_self_y <= start_ghost_y <= end_self_y)):
                if not self.is_seeker:
                    import sys
                    print("T'es trop con, t'es mort !")
                    sys.exit()
                ghost_group.remove(ghost)
                pass


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
