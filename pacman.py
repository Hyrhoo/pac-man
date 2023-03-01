<<<<<<< HEAD
"""
Programme réalisé par nom, prénom, classe
"""
import pygame

#variables du niveau
NB_TILES = 27   #nombre de tiles a chager (ici de 00.png à 26.png) 27 au total !!
TITLE_SIZE=32   #definition du dessin (carré)
largeur=8       #hauteur du niveau
hauteur=8       #largeur du niveau
tiles=[]       #liste d'images tiles

#variables de gestion du pacman
pacX=1          #position x y du pacman dans le niveau
pacY=1
compteurBilles=0

#variables de gestion du fantome
FRAMERATE_FANTOME= 120      #vitesse du fantome chiffre elevé = vitesse lente
NB_DEPLACEMENT_FANTOME =9   #le fantome se deplace sur 9 cases
positionFantome=1
frameRateCounterFantome=0
posfX=4     #position initiale du fantome
posfY=2

#definition du niveau

niveau=[[1,5,5,5,5,5,5,2],
     [6,0,12,12,12,12,12,6],
     [6,12,12,12,12,12,12,6],
     [6,12,12,12,12,12,12,6],
     [6,12,12,12,12,12,12,6],
     [6,12,12,12,12,12,12,6],
     [6,12,12,12,12,12,12,6],
     [3,5,5,5,5,5,5,4]]

fantome=[[0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0],
     [0,0,0,0,1,2,3,0],
     [0,0,0,0,8,0,4,0],
     [0,0,0,0,7,6,5,0],
     [0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0]]


#la taille de la fenetre dépend de la largeur et de la hauteur du niveau
#on rajoute une rangée de 32 pixels en bas de la fentre pour afficher le score d'ou (hauteur +1)
pygame.init()
fenetre = pygame.display.set_mode((largeur*TITLE_SIZE, (hauteur+1)*TITLE_SIZE))
pygame.display.set_caption("Pac-Man")
font = pygame.font.Font('freesansbold.ttf', 20)

def chargetiles(tiles):
    """
    fonction permettant de charger les images tiles dans une liste tiles[]
    """
    for n in range(0,NB_TILES):
        #print('data/'+str(n)+'.png')
        tiles.append(pygame.image.load('data/'+str(n)+'.png')) #attention au chemin


def afficheNiveau(niveau):
    """
    affiche le niveau a partir de la liste a deux dimensions niveau[][]
    """
    for y in range(hauteur):
        for x in range(largeur):
            fenetre.blit(tiles[niveau[y][x]],(x*TITLE_SIZE,y*TITLE_SIZE))


def affichePac(numero):
    """
    affiche le pacman en position pacX et pacY
    """
    fenetre.blit(tiles[numero],(pacX * TITLE_SIZE,pacY * TITLE_SIZE))

def afficheScore(score):
    """
    affiche le score
    """
    scoreAafficher = font.render(str(score), True, (0, 255, 0))
    fenetre.blit(scoreAafficher,(120,250))

def rechercheFantome(fantome,position): #recherche les coord du fantome dans la liste fantome
    """
    recherche les coordonnées du fantome en fonction du numéro de sa postion dans le parcours
    """
    print(position)                     #la position doit etre dans la liste fantome sinon plantage
    for y in range(hauteur):
        for x in range(largeur):
            if fantome[y][x]==position:
                coodFantome=x,y
    return coodFantome          #les coord du fantome x et y sont dans un tuple coodFantome

def deplaceFantome(fantome):
    """
    Incrémente automatiquement le déplacement du fantome, gère sa vitesse et son affichage
    """
    global frameRateCounterFantome
    global positionFantome
    global posfX,posfY
    if frameRateCounterFantome==FRAMERATE_FANTOME:      #ralenti la viteese du fantome
        posfX,posfY=rechercheFantome(fantome,positionFantome)   #deballage du tuple coordonnées du fantome
        positionFantome+=1
        if positionFantome==NB_DEPLACEMENT_FANTOME:     #un tour est fait donc on passe à la 1ere position
            positionFantome=1
        frameRateCounterFantome=0                       #compteur de vitesse à zero
    fenetre.blit(tiles[15],(posfX * TITLE_SIZE,posfY * TITLE_SIZE)) #affichage du fantome
    frameRateCounterFantome+=1                          #incrémentation du compteur de vitesse


chargetiles(tiles)  #chargement des images

loop=True
while loop==True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False            #fermeture de la fenetre (croix rouge)
        elif event.type == pygame.KEYDOWN:  #une touche a été pressée...laquelle ?
            if event.key == pygame.K_UP:    #est-ce la touche UP
                posY = pacY - 1             #on deplace le pacman vituellement
                posX = pacX
                numeroTile = niveau[posY][posX]       #on regarde le numéro du tile
                print("up",numeroTile,end=':')
                if (numeroTile == 12 or numeroTile == 0):   #si le tile est une bille ou un fond noir alors le déplacement est possible
                    pacY -= 1                               #on monte donc il faut décrémenter pacY
                    print("deplacement possible",pacX,pacY)
                else:
                    print("deplacement impossible")
            elif event.key == pygame.K_DOWN:  #est-ce la touche DOWN
                posY = pacY + 1
                posX = pacX
                numeroTile = niveau[posY][posX]
                print("down",numeroTile,end=':')
                if (numeroTile == 12 or numeroTile == 0):
                    pacY += 1
                    print("deplacement possible",pacX,pacY)
                else:
                    print("deplacement impossible")
            elif event.key == pygame.K_RIGHT:  #est-ce la touche RIGHT
                pass
                #A compléter pour le déplacement à droite

            elif event.key == pygame.K_LEFT:  #est-ce la touche LEFT
                pass
                #A compléter pour le déplacement à gauche

            elif event.key == pygame.K_ESCAPE or event.unicode == 'q': #touche q pour quitter
                loop = False
            if (numeroTile==12):  #si le numero du tile est 12 c'est que l'on est sur une nouvelle bille
                compteurBilles+=1   #alors on incrémente le score
                niveau[posY][posX]=0    #et on efface la bille dans le niveau
                print("nouvelle bille")
            else:
                print("fond noir")

    fenetre.fill((0,0,0))   #efface la fenetre
    afficheNiveau(niveau)   #affiche le niveau
    affichePac(14)          #affiche la pacman et le score
    deplaceFantome(fantome) #mettre un commentaire pour desactiver le déplacement du fantome
    afficheScore(compteurBilles)
    pygame.display.update() #mets à jour la fentre graphique
pygame.quit()

=======
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
        return self.map[y//TILE_SIZE][x//TILE_SIZE] in self.COLLISION


class Character:
    def __init__(self, pos_x, pos_y, image_path, labyrinth : Labyrinth):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        var = pygame.PixelArray(self.image.copy())
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
        
    def move(self, x, y):

        self.tp(x, y)
        print(x, y)
        if not self.labyrinth.is_colliding(self.pos_x + x,self.pos_y + y):
            self.pos_x += x
            self.pos_y += y
        print(self.pos_x, self.pos_y)


class Pac_man(Character):
    keys_directions = {pygame.K_UP: (0,-5), pygame.K_DOWN: (0,5), pygame.K_LEFT: (-5, 0), pygame.K_RIGHT: (5, 0)}
    
    def __init__(self, x, y, labyrinth, image_path = "data/pacman.png", direction = (5, 0)) -> None:
        Character.__init__(self, x, y, image_path, labyrinth)
        self.direction = direction
    
    def set_direction(self, keys):
        keys = [key.key for key in keys if key.type == pygame.KEYDOWN]
        for key, value in self.keys_directions.items():
            if key in keys:
                if value != self.direction:
                    if not self.labyrinth.is_colliding(self.pos_x + value[0], self.pos_y + value[1]):
                        self.direction = value

    def update(self, keys):
        self.set_direction(keys)
        self.move(self.direction[0], self.direction[1])
        self.draw_character()

class Ghost(Character):
    
    def __init__(self, x, y, labyrinth, image_path = "data/ghost.png") -> None:
        Character.__init__(self, x, y, image_path, labyrinth)


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
>>>>>>> 108e7efd19ad8262742eb06d7656736ddb20c2c8
