from pico2d import *

import game_framework
import game_world
import game_state
import random

Left, Right, Neutral = 0, 1, 2
first_floor_cat_y = 180

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Move_speed_MPS = 200
Move_speed_PPS = (Move_speed_MPS * Pixel_per_Meter)
Active_Range_x = 200
Magic_speed_MPS = 1000
Magic_speed_PPS = (Magic_speed_MPS * Pixel_per_Meter)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class IdleState:

    @staticmethod
    def enter(enemy, event):
        enemy.frame = 0

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        enemy.Attack_Timer += game_framework.frame_time
        if enemy.x < game_state.player.x:
            enemy.dir = Right
        elif enemy.x > game_state.player.x:
            enemy.dir = Left
        if enemy.Attack_Timer >= 8:
            enemy.Attack()
            enemy.Attack_Timer = 0

    @staticmethod
    def draw(enemy):
        if enemy.dir == Right:
            enemy.image.clip_draw(int(enemy.frame) * 120, 0, 120, 200, enemy.x, enemy.y)  # 오른쪽 이동
        else:
            enemy.image.clip_draw(int(enemy.frame) * 120, 0, 120, 200, enemy.x, enemy.y)

"""
class AttackState:

    @staticmethod
    def enter(enemy, event):
        enemy.frame = 0
        enemy.jump_max_height = 100
        enemy.jump_height_list = [enemy.y, enemy.y + enemy.jump_max_height]
        enemy.jumping_x = [enemy.x, enemy.x]
        enemy.jumping = False
        enemy.i = 0

    @staticmethod
    def exit(enemy, event):
        if event == RIGHT_DOWN:
            enemy.x_in_jumping += 3

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + 1) % 8
        if enemy.y <= enemy.ground_y + enemy.jump_max_height:
            enemy.i += 3
            t = enemy.i / 100
            enemy.y = (1 - t) * enemy.jump_height_list[0] + t * enemy.jump_height_list[1]
            enemy.x = (1 - t) * enemy.jumping_x[0] + t * enemy.jumping_x[1]
            enemy.image.clip_draw(enemy.frame * 61, 0, 61, 130, enemy.x, enemy.y)
        else:
            enemy.jumping is True
            enemy.add_event(5)

    @staticmethod
    def draw(enemy):
        if enemy.velocity == 2:
            enemy.image.clip_draw(enemy.frame * 61, 0, 61, 130, enemy.x, enemy.y)
        else:
            enemy.image.clip_draw(enemy.frame * 61, 0, 61, 130, enemy.x, enemy.y)  # 왼쪽 스프라이트
"""


class Enemy_cat:
    def __init__(self):
        self.x, self.y = 800, first_floor_cat_y
        self.ground_y = self.y
        self.image = load_image('resource\\High_cat.png')
        self.dir = Left
        self.Attack_Timer = 7
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.HP = 5
        self.exist = False
        self.magic = Magic(self.x, self.y)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return self.x - 60, self.y - 100, self.x + 60, self.y + 100

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        if not self.exist and game_state.background.block == 2:
            game_world.add_object(self, 1)
            self.exist = True
        if self.HP <= 0 or not game_state.background.block == 2:
            game_world.remove_object(self)
            self.exist = False

    def draw(self):
        if self.HP > 0:
            self.cur_state.draw(self)
            draw_rectangle(*self.get_bb())

    def input_buttons(self, event):
        pass

    def Attack(self):
        if not self.magic.exist:
            self.magic.exist = True
            self.magic.x, self.magic .y = self.x, self.y
            self.magic.shoot_dir = self.dir

            game_world.add_object(self.magic, 1)

    """
    def Attack(self):
        for i in range(10):
            if not self.magic[i].exist:
                self.magic[i].exist = True
                self.magic[i].x, self.magic[i].y = self.x, self.y
                self.magic[i].dir = self.dir

                self.arrow_num = clamp(0, i, 9)
                game_world.add_object(self.magic[i], 1)
                break
    """


class Magic:
    image = None

    def __init__(self, x, y):
        if Magic.image is None:
            Magic.image = load_image('resource\\RangeAttack.png')
        self.x, self.y, self.velocity = x, y, Magic_speed_MPS
        self.target_x, self.target_y = 0, 0
        self.exist = False
        self.shoot_dir = None

    def draw(self):
        if self.exist:
            self.image.draw(self.x, self.y)
            draw_rectangle(*self.get_bb())
            # print(self.velocity)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        self.target_x, self.target_y = game_state.player.x, game_state.player.y
        if self.exist:
            if self.shoot_dir == Left and self.x > self.target_x:
                self.x += -10
                self.y += random.randint(-10, 10)
            elif self.shoot_dir == Right and self.x < self.target_x:
                self.x += 10
                self.y += random.randint(-10, 10)

