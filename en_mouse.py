from pico2d import *

import game_world

first_floor_mouse_y = 80

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Move_speed_MPS = 5
Move_speed_PPS = (Move_speed_MPS * Pixel_per_Meter)


class IdleState:

    @staticmethod
    def enter(enemy, event):
        enemy.frame = 0

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + 1) % 8

    @staticmethod
    def draw(enemy):
        if enemy.dir == 1:
            enemy.image.clip_draw(enemy.frame * 61, 0, 280, 50, enemy.x, enemy.y)
        else:
            enemy.image.clip_draw(enemy.frame * 61, 0, 280, 50, enemy.x, enemy.y)


class MoveState:

    @staticmethod
    def enter(enemy, event):
        enemy.frame = 0
        enemy.dir = enemy.velocity

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + 1) % 8
        enemy.x += enemy.velocity
        enemy.x = clamp(25, enemy.x, 960)

    @staticmethod
    def draw(enemy):
        if enemy.velocity == 1:
            enemy.image.clip_draw(enemy.frame * 61, 0, 61, 130, enemy.x, enemy.y)
            delay(0.01)
        else:
            enemy.image.clip_draw(enemy.frame * 61, 0, 61, 130, enemy.x, enemy.y)  # 왼쪽 이동 스프라이트
            delay(0.01)


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


class Enemy:
    global first_floor_mouse_y

    def __init__(self):
        self.x, self.y = 800, first_floor_mouse_y  # 120은 지형의 높이.
        self.ground_y = self.y
        self.image = load_image('resource\\High_mouse.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def input_buttons(self, event):
        self.add_event(key_event)
        pass

