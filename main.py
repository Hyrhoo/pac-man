from scripts.initialisation import *
from scripts.labyrinth import *
from scripts.pacman import *
from scripts.ghost import *


def reset():
    """reset l'état du jeu

    Returns:
        pygame Groupe: groupe de joueur / fantôme
    """
    ghost_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    player = Pac_man(TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*23, labyrinth)

    blinky = Blinky(labyrinth, TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*11, type_hunt="hunt", timer_hunt=10_000)
    pinky = Pinky(labyrinth, TILE_SIZE*11 + TILE_SIZE//2, TILE_SIZE*14, type_hunt="hunt", timer_hunt=11_000)
    inky = Inky(labyrinth, TILE_SIZE*13 + TILE_SIZE//2, TILE_SIZE*14, type_hunt="hunt", timer_hunt=14_000)
    clyde = Clyde(labyrinth, TILE_SIZE*15 + TILE_SIZE//2, TILE_SIZE*14, type_hunt="hunt", timer_hunt=17_000)

    player_group.add(player)
    ghost_group.add(blinky)
    ghost_group.add(pinky)
    ghost_group.add(inky)
    ghost_group.add(clyde)

    return player_group, ghost_group

def display_lifes():
    pygame.draw.rect(screen, "#000000", pygame.Rect((TILE_SIZE*(WIDTH + 0.5), 50, TILE_SIZE, TILE_SIZE * 1.2 * lifes)))
    for l in range(lifes-1):
        screen.blit(life_image, ((TILE_SIZE*(WIDTH + 0.5), 50 + TILE_SIZE* 1.2 * l)))


def display_score():
    score_image = font.render(str(score), True,
                                    (255, 255, 255))
    size = font.size(str(score))
    pygame.draw.rect(screen, "#000000", pygame.Rect(TILE_SIZE*WIDTH+1, TILE_SIZE * HEIGHT // 2, TILE_SIZE*2,TILE_SIZE + size[1]))
    screen.blit(score_image, ((TILE_SIZE * (WIDTH + 1) - size[0] // 2, TILE_SIZE * HEIGHT // 2 + size[1])))

def display_end_message():
    message = "GAME OVER"
    font = pygame.font.SysFont("", 50)
    message_image = font.render(message,True, (255, 0, 0))
    size = font.size(message)
    screen.blit(message_image, ((TILE_SIZE * (WIDTH) // 2 - size[0] // 2, TILE_SIZE * HEIGHT // 2 - size[1])))

    # ==== init ==== #

life_image = pygame.transform.scale(pygame.image.load(f"{DATA_DIRECTORY}/pacman/4.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))

font = pygame.font.SysFont("", TILE_SIZE * 25 // 32)
labyrinth = Labyrinth(f"{DATA_DIRECTORY}/map.txt", screen)
score = 0

lifes = 3

sc_img = font.render("SCORE",True, (255, 255, 255))
size = font.size("SCORE")

screen.blit(sc_img, ((TILE_SIZE * (WIDTH + 1) - size[0] // 2, TILE_SIZE * HEIGHT // 2 - size[1])))

    # ==== main loop ==== #

run = True
while run and lifes:
    display_lifes()
    player_group, ghost_group = reset()
    labyrinth.draw_level()
    player_group.draw(screen)
    ghost_group.draw(screen)
    pygame.display.flip()
    pygame.time.wait(1000)
    game = True
    while game and run:
        display_score()
        labyrinth.draw_level()
        keys = pygame.event.get()
        for event in keys:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        for player in player_group:
            death, add_score = player.update(keys, ghost_group)
            if death:
                game = False
            score += add_score

        player_group.draw(screen)
        ghost_group.update(player_group.sprites()[0], ghost_group.sprites()[0])
        ghost_group.draw(screen)


        pygame.display.flip()

        if labyrinth.get_nbr_gommes() == 0:
            game = False
            run = False

        print(clock.get_fps())  # juste pour afficher les fps
        clock.tick(GLOBAL_FPS)
    lifes -= 1

display_end_message()
pygame.display.flip()
pygame.time.wait(500)

pygame.quit()
