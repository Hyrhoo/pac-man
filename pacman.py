import pygame
from time import monotonic

    # ==== variables ==== #

GLOBAL_FPS = 60     # FPS global du jeu
TILE_SIZE = 28      # definition du dessin (carré)
NUMBRE_IMG = 18     # nombre d'images à charger
length = 28         # hauteur du niveau
height = 31         # largeur du niveau

    # ==== classes ==== #

class Labyrinth:
    COLLISION = range(3, 19)
    def __init__(self, map_file):
        """
        initialise les données de la classe en chargeant d'abord les images puis les datas de la map


        Args:
            map_file (str): le nom du fichier à charger
        """
        self.load_tiles()
        self.load_map(map_file)


    def load_tiles(self):
        """
        charge les images nécessaires à l'affichage du labyrinthe
        """
        self.tiles = []
        for n in range(NUMBRE_IMG):
            self.tiles.append(pygame.transform.scale(pygame.image.load(f"data/{n}.png").convert(), (TILE_SIZE, TILE_SIZE)))
   
    def load_map(self, file):
        """
        charge le fichier contenant les datas de la map


        Args:
            file (str): le nom du fichier à charger
        """
        with open(file, "r") as f:
            self.map = []
            for line in f.readlines():
                self.map.append([int(i) for i in line.strip("\n").split()])
   
    def draw_level(self):
        """
        affiche le niveau a partir de la liste a deux dimensions self.map[][]
        """
        for y, ligne in enumerate(self.map):
            for x, case in enumerate(ligne):
                screen.blit(self.tiles[case], (x * TILE_SIZE, y * TILE_SIZE))
        pygame.draw.line(screen, "#FFFFFF", (length * TILE_SIZE, 0), (length * TILE_SIZE, height * TILE_SIZE))
   
    def is_colliding(self, x, y):
        return self.map[y][x] in self.COLLISION



class Character:
    def __init__(self, pos_x, pos_y, image_path, labyrinth : Labyrinth, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        var = pygame.PixelArray(self.image)
        var.replace((0, 0, 0, 255), (0, 0, 0, 0))
        self.labyrinth = labyrinth

    def draw_character(self):
        screen.blit(self.image, (self.pos_x, self.pos_y))

    def tp(self, x_pixels, y_pixels):
        if 0 > y_pixels + self.pos_y:
            self.pos_y = height - y_pixels
        if y_pixels + self.pos_y >= height * TILE_SIZE:
            self.pos_y = y_pixels - height * TILE_SIZE

        if 0 > x_pixels + self.pos_x:
            self.pos_x = length - x_pixels
        elif x_pixels + self.pos_x >= height * TILE_SIZE:
            self.pos_x = x_pixels - height * TILE_SIZE
        

    def can_move(self, x, y):
        new_pos_x = self.pos_x + x * self.speed
        new_pos_y = self.pos_y + y * self.speed
        if (x,y)!=(1,0):
            print(self.pos_x,self.pos_y)
            print(new_pos_x,new_pos_y)

        
        if self.direction == (-1, 0) and self.labyrinth.is_colliding(new_pos_x//TILE_SIZE, (new_pos_y+TILE_SIZE//2)//TILE_SIZE):
            if (x,y)!=(1,0):
                print(1)
            return False
        if self.direction == (0, -1) and self.labyrinth.is_colliding((new_pos_x+TILE_SIZE//2)//TILE_SIZE, new_pos_y//TILE_SIZE):
            if (x,y)!=(1,0):
                print(2)
            return False
        elif self.direction == (1, 0) and self.labyrinth.is_colliding((new_pos_x+TILE_SIZE)//TILE_SIZE, (new_pos_y+TILE_SIZE//2)//TILE_SIZE):
            if (x,y)!=(1,0):
                print(3)
            return False
        elif self.direction == (0, 1) and self.labyrinth.is_colliding((new_pos_x+TILE_SIZE//2)//TILE_SIZE, (new_pos_y+TILE_SIZE)//TILE_SIZE):
            if (x,y)!=(1,0):
                print(4)
            return False
        
        return True



    def move(self):
        x, y = self.direction
        self.tp(x, y)
        if self.can_move(x, y):
            self.pos_x += x * self.speed
            self.pos_y += y * self.speed
    


class Pac_man(Character):
    speed=5
    keys_directions = {pygame.K_UP: (0,-1), pygame.K_DOWN: (0,1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
    
    def __init__(self, x, y, labyrinth, image_path = "data/pacman.png", direction = (1, 0)) -> None:
        Character.__init__(self, x, y, image_path, labyrinth, direction)
    
    def set_direction(self, keys):
        keys = [key.key for key in keys if key.type == pygame.KEYDOWN]
        for key, value in self.keys_directions.items():
            if key in keys:
                if value != self.direction:
                    if self.can_move(value[0],value[1]):
                        self.direction = value

    def update(self, keys):
        self.set_direction(keys)
        self.move()
        self.draw_character()

class Ghost(Character):
    
    def __init__(self, x, y, labyrinth, image_path = "data/ghost.png", direction = (1,0)) -> None:
        Character.__init__(self, x, y, image_path, labyrinth, direction)


    # ==== fonctions ==== #



    # ==== init ==== #

pygame.init()
screen = pygame.display.set_mode((TILE_SIZE*(length+2), TILE_SIZE * height))
clock = pygame.time.Clock()

labyrinth = Labyrinth("map.txt")
player = Pac_man(TILE_SIZE * 13+TILE_SIZE//2,TILE_SIZE*23,labyrinth)
ghost = Ghost(1,1,labyrinth)

    # ==== main loop ==== #
pygame.key.set_repeat(0,0)
run = True
while run:
    labyrinth.draw_level()
    keys = pygame.event.get()
    for event in keys:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    player.update(keys)
    
    pygame.display.flip()
    #print(clock.get_fps())  # juste pour afficher les fps
    clock.tick(GLOBAL_FPS)

pygame.quit()
