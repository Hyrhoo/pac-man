from fonctions.initialisation import *
from fonctions.labyrinth import Labyrinth
from fonctions.character import Character

class Ghost(Character):
    direction_to_sens = {(-1,0): 0, (1,0): 1, (0,-1): 2, (0,1): 3}

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png",
                              "data/ghost_right_1.png", "data/ghost_right_2.png", "data/ghost_right_3.png", "data/ghost_right_4.png", "data/ghost_right_5.png", "data/ghost_right_6.png", "data/ghost_right_7.png",
                              "data/ghost_up_1.png", "data/ghost_up_2.png", "data/ghost_up_3.png", "data/ghost_up_4.png", "data/ghost_up_5.png", "data/ghost_up_6.png", "data/ghost_up_7.png",
                              "data/ghost_down_1.png", "data/ghost_down_2.png", "data/ghost_down_3.png", "data/ghost_down_4.png", "data/ghost_down_5.png", "data/ghost_down_6.png", "data/ghost_down_7.png"],
                 anim_len=7, direction=(-1,0), color=(255, 0, 0)) -> None:
        super().__init__(x, y, speed, direction, image_paths, labyrinth)
        self.anim_len = anim_len
        self.current_sens = self.direction_to_sens[self.direction]
        for image in self.sprites:
            pygame.PixelArray(image).replace((237, 28, 36, 255), color)

        # if self.can_move((self.pos_x+self.direction[0]*TILE_SIZE, self.pos_y+self.direction[1]*TILE_SIZE)):
        #     return
        # can be useful to forbid to the ghosts to go back while moving
    
    def update(self) -> None:
        self.current_sprite += 0.5
        if self.current_sprite >= self.anim_len:
            self.current_sprite -= self.anim_len
        self.image = self.sprites[int(self.current_sprite + self.current_sens*self.anim_len)]



class Blinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png",
                              "data/ghost_right_1.png", "data/ghost_right_2.png", "data/ghost_right_3.png", "data/ghost_right_4.png", "data/ghost_right_5.png", "data/ghost_right_6.png", "data/ghost_right_7.png",
                              "data/ghost_up_1.png", "data/ghost_up_2.png", "data/ghost_up_3.png", "data/ghost_up_4.png", "data/ghost_up_5.png", "data/ghost_up_6.png", "data/ghost_up_7.png",
                              "data/ghost_down_1.png", "data/ghost_down_2.png", "data/ghost_down_3.png", "data/ghost_down_4.png", "data/ghost_down_5.png", "data/ghost_down_6.png", "data/ghost_down_7.png"],
                 anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_paths, anim_len, direction, (255, 0, 0))


class Pinky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png",
                              "data/ghost_right_1.png", "data/ghost_right_2.png", "data/ghost_right_3.png", "data/ghost_right_4.png", "data/ghost_right_5.png", "data/ghost_right_6.png", "data/ghost_right_7.png",
                              "data/ghost_up_1.png", "data/ghost_up_2.png", "data/ghost_up_3.png", "data/ghost_up_4.png", "data/ghost_up_5.png", "data/ghost_up_6.png", "data/ghost_up_7.png",
                              "data/ghost_down_1.png", "data/ghost_down_2.png", "data/ghost_down_3.png", "data/ghost_down_4.png", "data/ghost_down_5.png", "data/ghost_down_6.png", "data/ghost_down_7.png"],
                 anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_paths, anim_len, direction, (255, 184, 255))


class Inky(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png",
                              "data/ghost_right_1.png", "data/ghost_right_2.png", "data/ghost_right_3.png", "data/ghost_right_4.png", "data/ghost_right_5.png", "data/ghost_right_6.png", "data/ghost_right_7.png",
                              "data/ghost_up_1.png", "data/ghost_up_2.png", "data/ghost_up_3.png", "data/ghost_up_4.png", "data/ghost_up_5.png", "data/ghost_up_6.png", "data/ghost_up_7.png",
                              "data/ghost_down_1.png", "data/ghost_down_2.png", "data/ghost_down_3.png", "data/ghost_down_4.png", "data/ghost_down_5.png", "data/ghost_down_6.png", "data/ghost_down_7.png"],
                 anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_paths, anim_len, direction, (0, 255, 255))


   
class Clyde(Ghost):

    def __init__(self, x, y, labyrinth: Labyrinth, speed=5,
                 image_paths=["data/ghost_left_1.png", "data/ghost_left_2.png", "data/ghost_left_3.png", "data/ghost_left_4.png", "data/ghost_left_5.png", "data/ghost_left_6.png", "data/ghost_left_7.png",
                              "data/ghost_right_1.png", "data/ghost_right_2.png", "data/ghost_right_3.png", "data/ghost_right_4.png", "data/ghost_right_5.png", "data/ghost_right_6.png", "data/ghost_right_7.png",
                              "data/ghost_up_1.png", "data/ghost_up_2.png", "data/ghost_up_3.png", "data/ghost_up_4.png", "data/ghost_up_5.png", "data/ghost_up_6.png", "data/ghost_up_7.png",
                              "data/ghost_down_1.png", "data/ghost_down_2.png", "data/ghost_down_3.png", "data/ghost_down_4.png", "data/ghost_down_5.png", "data/ghost_down_6.png", "data/ghost_down_7.png"],
                 anim_len=7, direction=(-1,0)) -> None:
        super().__init__(x, y, labyrinth, speed, image_paths, anim_len, direction, (255, 184, 81))