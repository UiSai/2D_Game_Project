from pico2d import *
import title_state
import game_state

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
            background.BG1.draw(640, 480)
        elif background.block == 2:
            background.BG2.draw(640, 480)
        elif background.block == 3:  # 올라가는 길
            background.BG3.draw(640, 480)
        elif background.block == 4:  # 올라온 길
            background.BG4.draw(640, 480)
        elif background.block == 5:  # 우두머리 직전
            background.BG5.draw(640, 480)
        elif background.block == 6:  # 우두머리
            background.BG6.draw(640, 480)


class Background:
    def __init__(self):
        self.BG1 = load_image('resource\\Background\\BG1.png')
        self.BG2 = load_image('resource\\Background\\BG2.png')
        self.BG3 = load_image('resource\\Background\\BG3.png')
        self.BG4 = load_image('resource\\Background\\BG4.png')
        self.BG5 = load_image('resource\\Background\\BG5.png')
        self.BG6 = load_image('resource\\Background\\BG6.png')
        self.first_floor_of_grass = 40
        self.first_floor_of_tree = 460
        self.block = 3

        if not title_state.easter:
            self.bgm = load_music('resource\\Sound\\bgm.mp3')
            self.bgm.set_volume(64)
            self.bgm.repeat_play()
        else:
            self.bgm = load_music('resource\\Sound\\bgm02.mp3')
            self.bgm.set_volume(64)
            self.bgm.repeat_play()

    def draw(self):
        Block.draw(self)

    def update(self):
        pass
