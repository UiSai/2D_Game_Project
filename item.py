from pico2d import *
import game_world
import game_framework
import player
from stage1_BG import Background


class Set:
    @staticmethod
    def enter():
        global background

        background = Background()

    @staticmethod
    def exit():
        pass

    @staticmethod
    def do():
        pass

    @staticmethod
    def draw():
        if background.block == 1:
            Item_Health(300, 100).draw()
        elif background.block == 2:
            Item_Health(500, 100).draw()


class Item_Health:
    image = None

    def __init__(self):
        if Item_Health.image is None:
            Item_Health.image = load_image("resource\\HP.png")
        self.x = 0
        self.y = 0
        self.exist = True

    def draw(self, x, y):
        self.x = x
        self.y = y
        if self.exist:
            self.image.draw(self.x, self.y)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def update(self):
        pass

    def effect(self):
        if player.Player.HP <= 4:
            player.Player.HP += 2
        elif player.Player.HP == 5:
            player.Player.HP += 1


