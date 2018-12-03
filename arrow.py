from pico2d import *
import game_world
import game_framework

Pixel_per_Meter = 1 / 5  # 1픽셀에 1.23미터
Arrow_speed_MPS = 3000
Arrow_speed_PPS = (Arrow_speed_MPS * Pixel_per_Meter)
Left, Right = 0, 1


class RangeAttack:
    image_r = None
    image_l = None

    def __init__(self, x, y):
        if RangeAttack.image_r is None and RangeAttack.image_l is None:
            RangeAttack.image_r = load_image('resource\\arrow_r.png')
            RangeAttack.image_l = load_image('resource\\arrow_l.png')
        self.x, self.y, self.velocity = x, y, Arrow_speed_MPS
        self.exist = False
        self.dir = None

    def draw(self):
        if self.exist:
            if self.dir == Right:
                self.image_r.draw(self.x, self.y)
                # draw_rectangle(*self.get_bb())
            elif self.dir == Left:
                self.image_l.draw(self.x, self.y)
                # draw_rectangle(*self.get_bb())
            # print(self.velocity)

    def get_bb(self):
        return self.x - 54, self.y - 13, self.x + 54, self.y + 13

    def update(self):
        if self.exist:
            if self.dir == Right:
                self.x += self.velocity * game_framework.frame_time
            else:
                self.x -= self.velocity * game_framework.frame_time

