from scripts.initialisation import *
from scripts.labyrinth import *
from scripts.pacman import *
from scripts.ghost import *

    # ==== init ==== #

player_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
labyrinth = Labyrinth(f"{DATA_DIRECTORY}/map.txt", screen)
player = Pac_man(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*23, labyrinth)

blinky = Blinky(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*11, labyrinth, speed=7)
pinky = Pinky(TILE_SIZE*11 + TILE_SIZE//2, TILE_SIZE*14, labyrinth, direction=(1, 0))
inky = Inky(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*14, labyrinth, direction=(0, -1))
clyde = Clyde(TILE_SIZE*15 + TILE_SIZE//2, TILE_SIZE*14, labyrinth, direction=(0, 1))

player_group.add(player)
ghost_group.add(blinky)
ghost_group.add(pinky)
ghost_group.add(inky)
ghost_group.add(clyde)

print(blinky.chasse(player), "\n")
print(pinky.chasse(player), "\n")
print(inky.chasse(player), "\n")
print(clyde.chasse(player), "\n")

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
    ghost_group.update(player)
    ghost_group.draw(screen)
    
    #blinky.chasse(player)
    #pinky.chasse(player)
    #inky.chasse(player)
    #clyde.chasse(player)

    pygame.display.flip()
    #print(clock.get_fps())  # juste pour afficher les fps
    clock.tick(GLOBAL_FPS)

pygame.quit()
