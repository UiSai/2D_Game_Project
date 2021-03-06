from pico2d import *

import game_framework
import game_world
import game_state

Left, Right, Neutral = 0, 1, 2
first_floor_mouse_y = 85

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Move_speed_MPS = 200
Move_speed_PPS = (Move_speed_MPS * Pixel_per_Meter)
Active_Range_x = 200

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

    @staticmethod
    def draw(enemy):
        if enemy.dir == Right:
            enemy.image.clip_draw(int(enemy.frame) * 61, 0, 280, 50, enemy.x, enemy.y)  # 오른쪽 이동
        else:
            enemy.image.clip_draw(int(enemy.frame) * 61, 0, 280, 50, enemy.x, enemy.y)


class MoveState:

    @staticmethod
    def enter(enemy, event):
        enemy.dir = Right
        enemy.velocity += Move_speed_PPS

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if enemy.x < enemy.start_x + Active_Range_x and enemy.dir == Right:
            enemy.x += enemy.velocity * game_framework.frame_time
        elif enemy.x > enemy.start_x + Active_Range_x and enemy.dir == Right:
            enemy.dir = Left
        elif enemy.x > enemy.start_x - Active_Range_x and enemy.dir == Left:
            enemy.x -= enemy.velocity * game_framework.frame_time
        elif enemy.dir < enemy.start_x - Active_Range_x and enemy.dir == Left:
            enemy.dir = Right
            enemy.x -= enemy.velocity * game_framework.frame_time

        enemy.Invincible()

    @staticmethod
    def draw(enemy):
        if enemy.dir == Right:
            enemy.image_r.draw(enemy.x, enemy.y)
        else:
            enemy.image_l.draw(enemy.x, enemy.y)  # 왼쪽 이동 스프라이트


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


class Enemy_mouse:
    def __init__(self):
        self.x, self.y = 800, first_floor_mouse_y  # 120은 지형의 높이.
        self.ground_y = self.y
        self.start_x = self.x
        self.image_r = load_image('resource\\High_mouse_r.png')
        self.image_l = load_image('resource\\High_mouse_l.png')
        self.dir = Neutral
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.HP = 7
        self.exist = False
        self.Invincible_Status = False
        self.Invincible_Timer = 0

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return self.x - 100, self.y - 25, self.x + 100, self.y + 25

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        if not self.exist and game_state.background.block == 1:
            game_world.add_object(self, 1)
            self.exist = True
        if self.HP <= 0 or not game_state.background.block == 1:
            game_world.remove_object(self)
            self.exist = False

    def Invincible(self):
        if self.Invincible_Status:
            self.Invincible_Timer += game_framework.frame_time
            if self.Invincible_Timer >= 0.8:
                self.Invincible_Status = False
                self.Invincible_Timer = 0

    def draw(self):
        if self.HP > 0:
            self.cur_state.draw(self)
            # draw_rectangle(*self.get_bb())

    def input_buttons(self, event):
        pass

