from pico2d import *
import game_world
import game_framework
import player
import game_state


class Item_Health:
    image = None

    def __init__(self, x, y):
        if Item_Health.image is None:
            Item_Health.image = load_image("resource\\HP.png")
        self.x = x
        self.y = y
        self.exist = False
        self.HP = 1

    def draw(self):
        if self.exist:
            self.image.draw(self.x, self.y)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def update(self):
        if not self.exist and game_state.background.block == 5:
            game_world.add_object(self, 1)
            self.exist = True
        if self.HP <= 0 or not game_state.background.block == 5:
            game_world.remove_object(self)
            self.exist = False

    #def effect(self):
    #    if player.Player().HP <= 4:
    #        player.Player().HP += 2
    #    elif player.Player().HP == 5:
    #        player.Player().HP += 1


