from pico2d import *

import game_world
import game_framework


class Block:
    @staticmethod
    def enter(background):
        pass

    @staticmethod
    def exit(background):
        pass

    @staticmethod
    def do(background):
        pass

    @staticmethod
    def draw(background):
        if background.block == 1:
            background.tree_1.draw(250, background.first_floor_of_tree)
            background.tree_2.draw(1000, background.first_floor_of_tree)

            background.grass.draw(150, background.first_floor_of_grass)
            background.grass.draw(450, background.first_floor_of_grass)
            background.grass.draw(700, background.first_floor_of_grass)
            background.grass.draw(950, background.first_floor_of_grass)
            background.grass.draw(1200, background.first_floor_of_grass)
        elif background.block == 2:
            background.tree_2.draw(1000, background.first_floor_of_tree)

            background.grass.draw(150, background.first_floor_of_grass)
            background.grass.draw(450, background.first_floor_of_grass)
            background.grass.draw(700, background.first_floor_of_grass)
            background.grass.draw(950, background.first_floor_of_grass)
            background.grass.draw(1200, background.first_floor_of_grass)


class Background:
    def __init__(self):
        self.grass = load_image('resource\\Background\\d_grass.png')
        self.tree_1 = load_image('resource\\Background\\tree.png')
        self.tree_2 = load_image('resource\\Background\\tree2.png')
        self.first_floor_of_grass = 40
        self.first_floor_of_tree = 460
        self.block = 1

    def draw(self):
        Block.draw(self)

    def update(self):
        pass
