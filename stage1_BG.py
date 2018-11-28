from pico2d import *

#import item

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

            #item.Item_Health(300, 100).draw()
        elif background.block == 2:
            background.tree_2.draw(1000, background.first_floor_of_tree)

            background.grass.draw(150, background.first_floor_of_grass)
            background.grass.draw(450, background.first_floor_of_grass)
            background.grass.draw(700, background.first_floor_of_grass)
            background.grass.draw(950, background.first_floor_of_grass)
            background.grass.draw(1200, background.first_floor_of_grass)


class Background:
    def __init__(self):
        self.grass = load_image('resource\\Background\\grass_modify.png')
        self.tree_1 = load_image('resource\\Background\\tree.png')
        self.tree_2 = load_image('resource\\Background\\tree2.png')
        self.first_floor_of_grass = 40
        self.first_floor_of_tree = 460
        self.block = 1
        """
        if not title_state.easter:
            self.bgm = load_music('resource\\Sound\\bgm.mp3')
            self.bgm.set_volume(64)
            self.bgm.repeat_play()
        else:
            self.bgm = load_music('resource\\Sound\\bgm02.mp3')
            self.bgm.set_volume(64)
            self.bgm.repeat_play()
        """

    def draw(self):
        Block.draw(self)

    def update(self):
        pass
