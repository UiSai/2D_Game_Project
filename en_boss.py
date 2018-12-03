from pico2d import *

import game_framework
import game_world
import game_state
import random

Left, Right, Up = 0, 1, 2
first_floor_boss_y = 180

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Move_speed_MPS = 200
Move_speed_PPS = (Move_speed_MPS * Pixel_per_Meter)
Knife_speed_MPS = 300
Knife_speed_PPS = (Knife_speed_MPS * Pixel_per_Meter)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class IdleState:

    @staticmethod
    def enter(enemy, event):
        enemy.frame = 0
        print('hello')

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        enemy.Idle_Timer += game_framework.frame_time
        if enemy.Idle_Timer >= 20:
            enemy.add_event(1)

    @staticmethod
    def draw(enemy):
        if enemy.dir == Right:
            enemy.image.clip_draw(int(enemy.frame) * 120, 0, 120, 200, enemy.x, enemy.y)  # 오른쪽 이동
        else:
            enemy.image.clip_draw(int(enemy.frame) * 120, 0, 120, 200, enemy.x, enemy.y)


count = 0

class AttackState:

    @staticmethod
    def enter(enemy, event):
        enemy.frame = 0
        print('enter')
        # Attack = Knife()

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        global count
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if enemy.exist:
            enemy.Attack_Timer += game_framework.frame_time
        else:
            enemy.Attack_Timer = 0
        """
        Attacks = [Knife() for i in range(10)]
        for Attack in Attacks:
            game_world.add_object(Attack, 1)
            Attack.update()
            Attack.draw()
            break
        """
        if enemy.Attack_Timer > 12:
            enemy.Attack_Timer = 0
            throw_dir = random.randint(0, 2)
            print(throw_dir)
            for i in range(10):
                # if not self.knife[i].exist:
                enemy.knife[i].exist = True
                enemy.knife[i].dir = throw_dir
                if enemy.knife[i].dir == Up:
                    enemy.knife[i].x, enemy.knife[i].y = random.randint(0, 1280), 960
                elif enemy.knife[i].dir == Right:
                    enemy.knife[i].x, enemy.knife[i].y = 1280, random.randint(0, 960)
                elif enemy.knife[i].dir == Left:
                    enemy.knife[i].x, enemy.knife[i].y = 0, random.randint(0, 960)

                enemy.knife_num = clamp(0, i, 9)
                game_world.add_object(enemy.knife[i], 2)
                count += 1
                if count > 30:
                    count = 0
                    enemy.add_event(0)
                #break



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
        self.HP = 50
        self.exist = False
        self.dead = False
        self.Invincible_Status = False
        self.Invincible_Timer = 0
        # self.knife = Knife()

        self.knife = [Knife() for i in range(10)]
        self.knife_num = 0
        self.damage = 1

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
        if self.HP <= 0:
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
        game_world.add_object(self.knife, 2)

    def Invincible(self):
        if self.Invincible_Status:
            self.Invincible_Timer += game_framework.frame_time
            if self.Invincible_Timer >= 0.8:
                self.Invincible_Status = False
                self.Invincible_Timer = 0

    """
    def Attack(self):
        for i in range(10):
            if not self.knife[i].exist:
                self.knife[i].exist = True
                self.knife[i].x, self.knife[i].y = self.x, self.y
                self.knife[i].dir = self.dir

                self.knife_num = clamp(0, i, 9)
                game_world.add_object(self.knife[i], 1)
                break
    """

"""
class Knife:
    image = None

    def __init__(self):
        if Knife.image is None:
            Knife.image = load_image('resource\\RangeAttack.png')
        self.x = random.randint(0, 1280)
        self.y = 950
        self.vertical_y = 960
        self.horizon_x1 = 0
        self.horizon_x2 = 1280
        self.velocity = Knife_speed_MPS
        self.target_x, self.target_y = 0, 0
        # self.exist = False
        self.shoot_dir = None
        self.Shoot_Timer = 0
        self.line_i = 0

    def draw(self):
        #if self.exist:
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        #if self.exist:
        print(self.x, self.y)
        self.Shoot_Timer += game_framework.frame_time
        print('시간', self.Shoot_Timer)
        if self.Shoot_Timer >= 5:
            self.y -= Knife_speed_PPS * game_framework.frame_time
            if self.y < -5:
                game_world.remove_object(self)
"""

class Knife:
    def __init__(self):
        self.image_right = load_image('resource\\sword_r.png')
        self.image_left = load_image('resource\\sword_l.png')
        self.image_up = load_image('resource\\sword_u.png')

        self.x, self.y, self.velocity = 0, 0, Knife_speed_PPS
        self.exist = False
        self.dir = None

    def draw(self):
        if self.exist:
            if self.dir == Right:
                self.image_right.draw(self.x, self.y)
                draw_rectangle(*self.get_bb())
            elif self.dir == Left:
                self.image_left.draw(self.x, self.y)
                draw_rectangle(*self.get_bb())
            elif self.dir == Up:
                self.image_up.draw(self.x, self.y)
                draw_rectangle(*self.get_bb())
            # print(self.velocity)

    def get_bb(self):
        if self.dir == Right or self.dir == Left:
            return self.x - 56, self.y - 16, self.x + 56, self.y + 16
        elif self.dir == Up:
            return self.x - 16, self.y - 56, self.x + 16, self.y + 56

    def update(self):
        if self.exist:
            if self.dir == Right:
                self.x -= self.velocity * game_framework.frame_time
            if self.dir == Left:
                self.x += self.velocity * game_framework.frame_time
            elif self.dir == Up:
                self.y -= self.velocity * game_framework.frame_time
