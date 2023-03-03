from fonctions.initialisation import *
from fonctions.labyrinth import Labyrinth
from fonctions.pacman import Pac_man
from fonctions.ghost import Blinky, Pinky, Inky, Clyde

    # ==== init ==== #

player_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
labyrinth = Labyrinth("map.txt")
player = Pac_man(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*23, labyrinth)

blinky = Blinky(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*11, labyrinth)
pinky = Pinky(TILE_SIZE*11 + TILE_SIZE//2, TILE_SIZE*14, labyrinth, direction=(1, 0))
inky = Inky(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*14, labyrinth, direction=(0, -1))
clyde = Clyde(TILE_SIZE*15 + TILE_SIZE//2, TILE_SIZE*14, labyrinth, direction=(0, 1))

player_group.add(player)
ghost_group.add(blinky)
ghost_group.add(pinky)
ghost_group.add(inky)
ghost_group.add(clyde)

    # ==== main loop ==== #

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

    player_group.update(keys)
    player_group.draw(screen)
    ghost_group.update()
    ghost_group.draw(screen)
    
    pygame.display.flip()
    #print(clock.get_fps())  # juste pour afficher les fps
    clock.tick(GLOBAL_FPS)

pygame.quit()
