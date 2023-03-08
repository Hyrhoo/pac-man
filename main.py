from scripts.initialisation import *
from scripts.labyrinth import *
from scripts.pacman import *
from scripts.ghost import *


def reset():
    ghost_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    player = Pac_man(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*23, labyrinth)


    blinky = Blinky(labyrinth, TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*11)
    pinky = Pinky(labyrinth, TILE_SIZE*11 + TILE_SIZE//2, TILE_SIZE*14, direction=(1, 0))
    inky = Inky(labyrinth, TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*14, direction=(0, -1))
    clyde = Clyde(labyrinth, TILE_SIZE*15 + TILE_SIZE//2, TILE_SIZE*14, direction=(0, 1))

    player_group.add(player)
    ghost_group.add(blinky)
    ghost_group.add(pinky)
    ghost_group.add(inky)
    ghost_group.add(clyde)

    return player_group, ghost_group

# ==== init ==== #


labyrinth = Labyrinth(f"{DATA_DIRECTORY}/map.txt", screen)

player_group, ghost_group = reset()

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

    player_group.update(keys, ghost_group)
    player_group.draw(screen)
    ghost_group.update(player_group.sprites()[0])
    ghost_group.draw(screen)

    pygame.display.flip()
    # print(clock.get_fps())  # juste pour afficher les fps
    clock.tick(GLOBAL_FPS)

pygame.quit()
