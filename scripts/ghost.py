from scripts.initialisation import *
from scripts.labyrinth import Labyrinth
from scripts.character import Character

class Ghost(Character):
    direction_to_sens = {(-1,0): 0, (1,0): 1, (0,-1): 2, (0,1): 3}
    spawn = (                (13,12),(14,12)                ,
             (11,13),(12,14),(13,13),(14,13),(15,13),(16,13),
             (11,14),(12,13),(13,14),(14,14),(15,14),(16,14),
             (11,15),(12,15),(13,15),(14,15),(15,15),(16,15))

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, type_hunt="dicipe", timer_hunt=2500, speed=10, direction=(-1,0), time_in_spawn=0, color=(255, 0, 0)) -> None:
        super().__init__(x, y, speed, direction, labyrinth)
        self.base_speed = self.speed
        self.current_sens = self.direction_to_sens[self.direction]
        self.current_cell = None
        
        self.in_spawn = self.get_actual_cell() in self.spawn
        self.can_go_out = False
        self.time_in_spawn = pygame.time.get_ticks() + time_in_spawn
        
        self.is_weaken = False
        self.time_weaken = 0

        self.type_hunt = type_hunt
        self.timer_hunt = timer_hunt + (pygame.time.get_ticks() if self.type_hunt == "hunt" else 0)
        self.can_change_hunt = True if self.type_hunt == "hunt" else False
        self.can_change_direction = False
        
        for image in self.sprites:
            pygame.PixelArray(image).replace((237, 28, 36, 255), color)

    def __repr__(self):
        """pratique pour les print

        Returns:
            str: les infos du fantôme
        """
        return f"{type(self)} - {(self.pos_x, self.pos_y)}, {self.get_actual_cell()}, {self.labyrinth.map[self.get_actual_cell()[1]][self.get_actual_cell()[0]]} - {self.direction} - {self.in_spawn}, {self.can_go_out}, {self.time_in_spawn}"

    def load_sprites(self):
        """charge les différentes images nécessaires pour l'affichage du fantôme"""
        for direction in ("left", "right", "up", "down", "weaken"):
            for nbr_img in range(1, NUMBER_IMG_GHOSTS+1):
                self.load_sprite(f"ghost/{direction}/{nbr_img}")
    
    def change_direction(self, new_direction):
        """permet au fantôme de changer de dirrection

        Args:
            new_direction (tuple[int]): la nouvelle direction à prendre
        """
        self.direction = new_direction
        self.current_sens = self.direction_to_sens[self.direction]
        pos = self.pos_in_laby(*self.get_front_pos(self.pos_x, self.pos_y, self.direction))
        self.reset_direction(pos)
    
    def get_possible_cells(self):
        """renvois les cases où peut ce déplacer le fantôme"""
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
        if self.can_change_direction:
            return cells
        return tuple(filter(fonc, cells))
    
    def direction_to_take(self, x, y):
        """savoir la direction à prendre pour ce diriger vers la case donner

        Args:
            x (int): position x de la case voulu
            y (int): position y de la case voulu

        Returns:
            tuple[int]: la dirrection à prendre pour rejoindre la case
        """
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
        """détermine la tuile où le fantôme doit ce déplacer

        Args:
            possible_move (tuple[tuple[int]]): tuple avec toutes les casses où le fantôme peut ce déplacer
            best_move (tuple[int]): le meilleur endroit où le fantôme pourrais allez

        Returns:
            tuple[int]: la position que le fantôme vas devoire rejoindre
        """
        if best_move in possible_move:
            return best_move
        return random.choice(possible_move)

    def animation(self):
        """anime le fantôme"""
        if self.is_weaken:
            self.current_sens = 4
        self.current_sprite += 1
        if self.current_sprite >= NUMBER_IMG_GHOSTS:
            self.current_sprite -= NUMBER_IMG_GHOSTS
        self.image = self.sprites[int(self.current_sprite + self.current_sens*NUMBER_IMG_GHOSTS)]
    
    def move_gestion(self, player, blinky):
        actual_cell = self.get_actual_cell()
        if (self.current_cell != actual_cell and self.labyrinth.is_intersect(*actual_cell)) or self.can_change_direction:
            self.current_cell = actual_cell
            possible_move = self.get_possible_cells()
            best_move = self.hunt(player, blinky)[1]
            tile = self.next_tile_to_take(possible_move, best_move)
            direction = self.direction_to_take(*tile)
            self.change_direction(direction)
            self.can_change_direction = False
        self.move(self.in_spawn)
    
    def spawn_gestion(self):
        if self.in_spawn:
            if self.time_in_spawn <= pygame.time.get_ticks():
                self.can_go_out = True
            if self.get_actual_cell() not in self.spawn:
                self.in_spawn = False
                self.can_go_out = False
                self.direction = (-1, 0)

    def weaken_gestion(self):
        if self.is_weaken:
            if pygame.time.get_ticks() >= self.time_weaken:
                self.type_hunt = "hunt"
                self.timer_hunt = pygame.time.get_ticks() + random.randint(8000, 12000)
                self.speed = self.base_speed
                self.is_weaken = False
                self.current_sens = self.direction_to_sens[self.direction]
    
    def hunt_mode_gestion(self):
        if self.can_change_hunt:
            if self.timer_hunt <= pygame.time.get_ticks():
                if self.type_hunt == "hunt":
                    self.timer_hunt = 2500
                    self.type_hunt = "dicipe"
                    self.can_change_hunt = False
                elif self.type_hunt == "dicipe":
                    self.timer_hunt = pygame.time.get_ticks() + random.randint(8000, 12000)
                    self.type_hunt = "hunt"
                    self.can_change_hunt = True
                self.can_change_direction = True
        elif self.get_actual_cell() == self.dispersion_point:
            self.timer_hunt += pygame.time.get_ticks()
            self.can_change_hunt = True
    
    def update(self, player, blinky) -> None:
        """fonction qui met à joure le fantôme d'une frame à l'autre

        Args:
            player (Pacman): le joueur à rechercher
        """
        self.animation()
        self.move_gestion(player, blinky)
        self.spawn_gestion()
        self.weaken_gestion()
        self.hunt_mode_gestion()

    def hunt(self, destination):
        """chasse le joueur

        Args:
            destination (tuple[int]): la position à rejoindre

        Returns:
            list[tuple[int]]: le chemain le plus court jusqu'à la position donner
        """
        pos = self.get_actual_cell()
        wall = [self.labyrinth.normalize_pos(pos[0]-self.direction[0], pos[1]-self.direction[1])]
        return self.labyrinth.astar(pos, destination, wall, self.in_spawn)

    def weaken(self, time):
        """rand le fantôme faible au joueur pour un temps donner

        Args:
            time (int): temps de faiblaisse en miliseconde
        """
        self.speed = self.base_speed * 0.6
        self.is_weaken = True
        self.time_weaken = pygame.time.get_ticks() + time


class Blinky(Ghost):
    dispersion_point = (26, 1)

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, type_hunt="dicipe", timer_hunt=4000, speed=8.5, direction=(-1,0), time_in_spawn=0) -> None:
        super().__init__(labyrinth, x, y, type_hunt, timer_hunt, speed, direction, time_in_spawn, (255, 0, 0))
    
    def hunt(self, player:Character, blinky:Ghost):
        """chasse le joueur

        Args:
            player (Character): le joueur à chasser

        Returns:
            list[tuple[int]]: le chemain le plus court pour aller juqu'au joueur
        """
        if self.type_hunt == "dicipe":
            destination = self.dispersion_point
        elif self.type_hunt == "hunt":
            destination = player.get_actual_cell()
        return super().hunt(destination)


class Pinky(Ghost):
    dispersion_point = (1, 1)

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, type_hunt="dicipe", timer_hunt=4000, speed=8.5, direction=(-1,0), time_in_spawn=0) -> None:
        super().__init__(labyrinth, x, y, type_hunt, timer_hunt, speed, direction, time_in_spawn, (255, 184, 255))

    def hunt(self, player:Character, blinky:Ghost):
        """chasse le joueur

        Args:
            player (Character): le joueur à chasser

        Returns:
            list[tuple[int]]: le chemain le plus court pour aller juqu'au joueur
        """
        if self.type_hunt == "dicipe":
            destination = self.dispersion_point
        elif self.type_hunt == "hunt":
            destination = player.get_actual_cell()
            destination = (destination[0] + player.direction[0]*4, destination[1] + player.direction[1]*4)
        return super().hunt(destination)


class Inky(Ghost):
    dispersion_point = (26, 29)

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, type_hunt="dicipe", timer_hunt=4000, speed=8.5, direction=(-1,0), time_in_spawn=2500) -> None:
        super().__init__(labyrinth, x, y, type_hunt, timer_hunt, speed, direction, time_in_spawn, (0, 255, 255))
    
    def hunt(self, player:Character, blinky:Ghost):
        """chasse le joueur

        Args:
            player (Character): le joueur à chasser

        Returns:
            list[tuple[int]]: le chemain le plus court pour aller juqu'au joueur
        """
        if self.type_hunt == "dicipe":
            destination = self.dispersion_point
        elif self.type_hunt == "hunt":
            player_pos = player.get_actual_cell()
            blinky_pos = blinky.get_actual_cell()
            blinky_player = (((player_pos[0] + player.direction[0]*2) - blinky_pos[0])*2, ((player_pos[1] + player.direction[1]*2) - blinky_pos[1])*2)
            destination = (blinky_pos[0] + blinky_player[0], blinky_pos[1] + blinky_player[1])
        return super().hunt(destination)


   
class Clyde(Ghost):
    dispersion_point = (1, 29)

    def __init__(self, labyrinth: Labyrinth, x=TILE_SIZE*13 + TILE_SIZE//2, y=TILE_SIZE*14, type_hunt="dicipe", timer_hunt=4000, speed=8.5, direction=(-1,0), time_in_spawn=5000) -> None:
        super().__init__(labyrinth, x, y, type_hunt, timer_hunt, speed, direction, time_in_spawn, (255, 184, 81))
    
    def hunt(self, player:Character, blinky:Ghost):
        """chasse le joueur

        Args:
            player (Character): le joueur à chasser

        Returns:
            list[tuple[int]]: le chemain le plus court pour aller juqu'au joueur
        """
        if self.type_hunt == "dicipe":
            destination = self.dispersion_point
        elif self.type_hunt == "hunt":
            player_pos = player.get_actual_cell()
            self_pos = self.get_actual_cell()
            distence = ((self_pos[0]-player_pos[0])**2 + (self_pos[1]-player_pos[1])**2)**0.5
            if distence >= 8:
                destination = player_pos
            else:
                destination = self.dispersion_point
        return super().hunt(destination)
