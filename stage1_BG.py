from pico2d import *

import game_world
import game_framework

class Background:
    def __init__(self):
        self.grass = load_image('resource\\Background\\d_grass.png')
        self.tree_1 = load_image('resource\\Background\\tree.png')
        self.tree_2 = load_image('resource\\Background\\tree2.png')
        self.first_floor_of_grass = 40
        self.first_floor_of_tree = 460

    def draw(self):
        self.tree_1.draw(250, self.first_floor_of_tree)
        self.tree_2.draw(1000, self.first_floor_of_tree)

        self.grass.draw(150, self.first_floor_of_grass)
        self.grass.draw(450, self.first_floor_of_grass)
        self.grass.draw(700, self.first_floor_of_grass)
        self.grass.draw(950, self.first_floor_of_grass)
        self.grass.draw(1200, self.first_floor_of_grass)

    def update(self):
        pass
