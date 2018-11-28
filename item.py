from pico2d import *
import game_world
import game_framework
import player


class Item_Health:
    image = None

    def __init__(self, x, y):
        if Item_Health.image is None:
            Item_Health.image = load_image("resource\\HP.png")
        self.exist = True
        self.x = x
        self.y = y

    def draw(self):
        if self.exist:
            self.image.draw(self.x, self.y)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def update(self):
        pass

    def effect(self):
        player.Player.HP += 2

