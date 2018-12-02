from pico2d import *
import game_world
import game_framework

Pixel_per_Meter = 1 / 5  # 1픽셀에 1.23미터
Arrow_speed_MPS = 1500
Arrow_speed_PPS = (Arrow_speed_MPS * Pixel_per_Meter)
Left, Right = 0, 1


class RangeAttack:
    image = None

    def __init__(self, x, y):
        if RangeAttack.image is None:
            RangeAttack.image = load_image('resource\\RangeAttack.png')
        self.x, self.y, self.velocity = x, y, Arrow_speed_MPS
        self.exist = False
        self.dir = None

    def draw(self):
        if self.exist:
            self.image.draw(self.x, self.y)
            draw_rectangle(*self.get_bb())
            # print(self.velocity)

    def get_bb(self):
        return self.x - 10, self.y - 100, self.x + 10, self.y + 100

    def update(self):
        if self.exist:
            if self.dir == Right:
                self.x += self.velocity * game_framework.frame_time
            else:
                self.x -= self.velocity * game_framework.frame_time

