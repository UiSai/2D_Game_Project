from pico2d import *

import game_framework
import game_world
import game_state
import random

Left, Right, Neutral = 0, 1, 2
first_floor_boss_y = 180

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Move_speed_MPS = 200
Move_speed_PPS = (Move_speed_MPS * Pixel_per_Meter)
Knife_speed_MPS = 100
Knife_speed_PPS = (Knife_speed_MPS * Pixel_per_Meter)

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
        enemy.Idle_Timer += game_framework.frame_time
        if enemy.Idle_Timer >= 5:
            enemy.add_event(1)

    @staticmethod
    def draw(enemy):
        if enemy.dir == Right:
            enemy.image.clip_draw(int(enemy.frame) * 120, 0, 120, 200, enemy.x, enemy.y)  # 오른쪽 이동
        else:
            enemy.image.clip_draw(int(enemy.frame) * 120, 0, 120, 200, enemy.x, enemy.y)


class AttackState:

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
            print('attack')
            enemy.Attack_Timer = 0

    @staticmethod
    def draw(enemy):
        if enemy.dir == Right:
            enemy.image.clip_draw(int(enemy.frame) * 120, 0, 120, 200, enemy.x, enemy.y)  # 오른쪽 이동
        else:
            enemy.image.clip_draw(int(enemy.frame) * 120, 0, 120, 200, enemy.x, enemy.y)


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

    @staticmethod
    def draw(enemy):
        if enemy.dir == Right:
            enemy.image.clip_draw(int(enemy.frame) * 0, 0, 280, 50, enemy.x, enemy.y)
        else:
            enemy.image.clip_draw(int(enemy.frame) * 0, 0, 280, 50, enemy.x, enemy.y)  # 왼쪽 이동 스프라이트


state_table = [IdleState, AttackState, MoveState]


class Enemy_boss:
    def __init__(self):
        self.x, self.y = 800, first_floor_boss_y
        self.ground_y = self.y
        self.image = load_image('resource\\High_boss.png')
        self.dir = Left
        self.Idle_Timer = 0
        self.Attack_Timer = 7
        self.Move_Timer = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = AttackState
        self.cur_state.enter(self, None)
        self.HP = 5
        self.exist = False
        self.dead = False
        self.knife = Knife()

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return self.x - 60, self.y - 100, self.x + 60, self.y + 100

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = state_table[event]
            self.cur_state.enter(self, event)
        if not self.exist and game_state.background.block == 6:
            game_world.add_object(self, 1)
            self.exist = True
        if self.HP <= 0 or not game_state.background.block == 6:
            game_world.remove_object(self)
            self.exist = False

    def draw(self):
        if self.HP > 0:
            self.cur_state.draw(self)
            draw_rectangle(*self.get_bb())

    def input_buttons(self, event):
        pass

    def Attack(self):
        self.knife.exist = True
        self.knife.x, self.knife.y = self.x, self.y
        self.knife.target_x, self.knife.target_y = game_state.player.x, game_state.player.y
        self.knife.line_i = 0
        self.knife.shoot_dir = self.dir

        game_world.add_object(self.knife, 1)

    """
    def Attack(self):
        for i in range(10):
            if not self.knife[i].exist:
                self.knife[i].exist = True
                self.knife[i].x, self.knife[i].y = self.x, self.y
                self.knife[i].dir = self.dir

                self.arrow_num = clamp(0, i, 9)
                game_world.add_object(self.knife[i], 1)
                break
    """


class Knife:
    image = None

    def __init__(self):
        if Knife.image is None:
            Knife.image = load_image('resource\\RangeAttack.png')
        self.x = random.randint(0, 1280)
        self.y = 960
        self.vertical_y = 960
        self.horizon_x1 = 0
        self.horizon_x2 = 1280
        self.velocity = Knife_speed_MPS
        self.target_x, self.target_y = 0, 0
        self.exist = False
        self.shoot_dir = None
        self.Shoot_Timer = 2
        self.line_i = 0

    def draw(self):
        if self.exist:
            self.image.draw(self.x, self.y)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        if self.exist:
            self.Shoot_Timer += game_framework.frame_time
            if self.Shoot_Timer >= 2:
                self.y -= Knife_speed_PPS
                self.Shoot_Timer = 0

