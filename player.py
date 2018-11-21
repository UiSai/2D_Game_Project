from pico2d import *
from arrow import Arrow
#from temp_rangeattack import RangeAttack

import game_world
import game_framework

first_floor_player_y = 130
Left, Right, Up, Fall, Neutral = 0, 1, 2, 3, 4

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Move_speed_MPS = 500
Move_speed_PPS = (Move_speed_MPS * Pixel_per_Meter)
Air_speed_MPS = 1000
Air_speed_PPS = (Air_speed_MPS * Pixel_per_Meter)
Rise_speed_PPS = (200 * Pixel_per_Meter)
Fall_speed_PPS = (500 * Pixel_per_Meter)

Arrow_speed_MPS = 15
Arrow_speed_PPS = (Arrow_speed_MPS * Pixel_per_Meter)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


Right_DOWN, Left_DOWN, Right_UP, Left_UP, Up_DOWN, Up_UP, Air_DOWN, MAttack, RAttack = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): Right_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): Left_DOWN,
    (SDL_KEYDOWN, SDLK_UP): Up_DOWN,
    (SDL_KEYDOWN, SDLK_a): Air_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): Right_UP,
    (SDL_KEYUP, SDLK_LEFT): Left_UP,
    (SDL_KEYUP, SDLK_UP): Up_UP,
    (SDL_KEYDOWN, SDLK_z): MAttack,
    (SDL_KEYDOWN, SDLK_x): RAttack
}

"""
class IdleState:

    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.velocity += Move_speed_PPS
        elif event == Left_DOWN:
            player.velocity -= Move_speed_PPS
        elif event == Right_UP:
            player.velocity -= Move_speed_PPS
        elif event == Left_UP:
            player.velocity += Move_speed_PPS
        elif event == Air_DOWN:
            player.y += 10

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        if player.dir == Right:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
"""


class GroundState:

    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.velocity += Move_speed_PPS
        elif event == Left_DOWN:
            player.velocity -= Move_speed_PPS
        elif event == Right_UP:
            player.velocity -= Move_speed_PPS
        elif event == Left_UP:
            player.velocity += Move_speed_PPS
        elif event == Air_DOWN:
            player.y += 10

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.velocity * game_framework.frame_time
        player.x = clamp(25, player.x, 1255)

    @staticmethod
    def draw(player):
        if player.velocity > 0:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 걷기 오른쪽 이동
        elif player.velocity < 0:
            player.image.clip_draw(int(player.frame) * 61, 130, 61, 130, player.x, player.y)  # 걷기 왼쪽 이동
        else:
            if player.dir == Right:
                player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 오른쪽을 보고 서있다
            elif player.dir == Left:
                player.image.clip_draw(int(player.frame) * 61, 130, 61, 130, player.x, player.y)  # 왼쪽을 보고 서있다

"""
class AirState:

    @staticmethod
    def enter(player, event):
        player.In_Air = True  # 정확한 False 처리가 필요함.(현재는 일부 State의 enter에서 처리중)
        if event == Right_DOWN:
            player.dir = Right
            player.velocity += Air_speed_PPS
        elif event == Left_DOWN:
            player.dir = Left
            player.velocity -= Air_speed_PPS
        elif event == Right_UP:
            player.dir = Neutral
            player.velocity -= Air_speed_PPS
        elif event == Left_UP:
            player.dir = Neutral
            player.velocity += Air_speed_PPS
        elif event == Up_DOWN:
            player.dir = Up
            player.Rise_velocity += Rise_speed_PPS
        elif event == Up_UP:
            player.dir = Neutral
            player.Rise_velocity -= Rise_speed_PPS

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        if player.dir == Right:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트
"""


class AirState:

    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.velocity += Air_speed_PPS
        elif event == Left_DOWN:
            player.velocity -= Air_speed_PPS
        elif event == Right_UP:
            player.velocity -= Air_speed_PPS
        elif event == Left_UP:
            player.velocity += Air_speed_PPS

        if event == Up_DOWN:
            player.Rise_velocity += Rise_speed_PPS
        elif event == Up_UP:
            player.Rise_velocity -= Rise_speed_PPS

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.velocity * game_framework.frame_time
        player.x = clamp(25, player.x, 1255)  # 넘어가면 강제로 조절함
        player.y += player.Rise_velocity * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.velocity < 0:
            player.dir = Left
            player.image.clip_draw(int(player.frame) * 61, 130, 61, 130, player.x, player.y)  # 공중 왼쪽 이동
        elif player.velocity > 0:
            player.dir = Right
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 공중 오른쪽 이동
        else:
            if player.Rise_velocity > 0:
                if player.dir == Left:
                    player.image.clip_draw(int(player.frame) * 61, 130, 61, 130, player.x, player.y)  # 왼쪽을 보는 상승
                elif player.dir == Right:
                    player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 오른쪽을 보는 상승
            else:
                if player.dir == Left:
                    player.image.clip_draw(int(player.frame) * 61, 130, 61, 130, player.x, player.y)  # 왼쪽을 보고 서있다
                elif player.dir == Right:
                    player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 오른쪽을 보고 서있다


class FallingState:

    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.velocity += Move_speed_PPS
        elif event == Left_DOWN:
            player.velocity -= Move_speed_PPS
        elif event == Right_UP:
            player.velocity -= Move_speed_PPS
        elif event == Left_UP:
            player.velocity += Move_speed_PPS

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if player.y >= player.ground_y:
            player.y -= Fall_speed_PPS * game_framework.frame_time
            if player.dir == Right:
                player.x += Move_speed_PPS * game_framework.frame_time
            elif player.dir == Left:
                player.x -= Move_speed_PPS * game_framework.frame_time
        else:
            player.In_Air = False
            player.cur_state = GroundState

    @staticmethod
    def draw(player):
        if player.dir == Right:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 61, 130, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


next_state_table = {
    GroundState: {Right_UP: GroundState, Left_UP: GroundState, Left_DOWN: GroundState, Right_DOWN: GroundState,
                  Air_DOWN: AirState, RAttack: GroundState, Up_DOWN: GroundState, Up_UP: GroundState},
    AirState: {Right_UP: AirState, Left_UP: AirState, Right_DOWN: AirState, Left_DOWN: AirState,
               Air_DOWN: FallingState, RAttack: AirState, Up_DOWN: AirState, Up_UP: AirState},
    FallingState: {Right_DOWN: FallingState, Left_DOWN: FallingState, Right_UP: FallingState, Left_UP: FallingState,
                   Air_DOWN: AirState, RAttack: FallingState, Up_DOWN: FallingState, Up_UP: FallingState}
}
"""
next_state_table = {
    IdleState: {Right_UP: MoveState, Left_UP: MoveState, Right_DOWN: MoveState, Left_DOWN: MoveState,
                Air_DOWN: AirState, RAttack: IdleState, Up_DOWN: IdleState, Up_UP: IdleState},
    MoveState: {Right_UP: IdleState, Left_UP: IdleState, Left_DOWN: IdleState, Right_DOWN: IdleState,
                Air_DOWN: AirState, RAttack: MoveState, Up_DOWN: MoveState, Up_UP: MoveState},
    AirState: {Right_UP: AirMoveState, Left_UP: AirMoveState, Right_DOWN: AirMoveState, Left_DOWN: AirMoveState,
               Air_DOWN: FallingState, RAttack: AirState, Up_DOWN: AirMoveState, Up_UP: AirMoveState},
    AirMoveState: {Right_UP: AirMoveState, Left_UP: AirMoveState, Left_DOWN: AirMoveState, Right_DOWN: AirMoveState,
                   Up_DOWN: AirMoveState, Up_UP: AirMoveState, Air_DOWN: FallingState},
    FallingState: {Right_DOWN: FallingState, Left_DOWN: FallingState, Right_UP: FallingState, Left_UP: FallingState,
                   Air_DOWN: AirState, RAttack: FallingState, Up_DOWN: FallingState, Up_UP: FallingState}
}
"""


class Player:
    def __init__(self):
        self.x, self.y = 100, first_floor_player_y  # 130은 지형의 높이.
        self.ground_y = self.y
        self.image = load_image('resource\\Character_sprite\\Player_animation.png')
        self.dir = Right
        self.velocity = 0
        self.Rise_velocity = 0
        self.Falling_velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = GroundState
        self.cur_state.enter(self, None)
        self.In_Air = False
        self.Exist_rangeattack = False

    def add_event(self, event):
        self.event_que.insert(0, event)

    def MeleeAttack(self):
        pass

    def RangeAttack(self):
        arrow = Arrow(self.x, self.y)
        game_world.add_object(arrow, 2)
        self.Exist_rangeattack = True
        print('pause')

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        print(self.dir)

    def draw(self):
        self.cur_state.draw(self)

    def input_buttons(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


"""
class RangeAttack:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if RangeAttack.image == None:
            RangeAttack.image = load_image('resource\\RangeAttack.png')
        self.x, self.y, self.velocity = x, y, RangeAttack_speed_PPS

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
"""
