from pico2d import *
import game_world
import game_framework

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Arrow_speed_MPS = 15
Arrow_speed_PPS = (Arrow_speed_MPS * Pixel_per_Meter)


class Arrow():
    image = None

    def __init__(self, x, y):
        if Arrow.image == None:
            Arrow.image = load_image('resource\\RangeAttack.png')
        self.x, self.y, self.velocity = x, y, Arrow_speed_PPS

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        print(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y - 100, self.x + 10, self.y + 100

    def update(self):
        self.x += self.velocity * game_framework.frame_time
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)