from pico2d import *
#from temp_rangeattack import RangeAttack

import game_world
import game_framework

first_floor_player_y = 130

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Run_speed_MPS = 5
Run_speed_PPS = (Run_speed_MPS * Pixel_per_Meter)
Air_speed_MPS = 10
Air_speed_PPS = (Air_speed_MPS * Pixel_per_Meter)
Rise_speed_PPS = (2 * Pixel_per_Meter)

RangeAttack_speed_MPS = 15
RangeAttack_speed_PPS = (RangeAttack_speed_MPS * Pixel_per_Meter)

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


class IdleState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.In_Air = False

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)


class MoveState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        # player.dir = player.velocity
        player.In_Air = False

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.velocity
        player.x = clamp(25, player.x, 960)
        print(player.velocity)

    @staticmethod
    def draw(player):
        if player.velocity == Run_speed_PPS:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 걷기 오른쪽 이동
        else:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 걷기 왼쪽 이동


class AirState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.In_Air = True  # 정확한 False 처리가 필요함.(현재는 일부 State의 enter에서 처리중)

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        print(player.In_Air)

    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


class AirMoveState:

    @staticmethod
    def enter(player, event):
        player.frame = 0

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.velocity
        player.x = clamp(25, player.x, 960)
        if player.dir == 2:
            player.y += player.Rise_velocity

    @staticmethod
    def draw(player):
        if player.velocity > Air_speed_PPS:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 공중 오른쪽 이동
        elif player.dir == 2:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 상승
        else:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 공중 왼쪽 이동


class FallingState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.fall_calculate_list = [player.x, player.y, player.ground_y]
        player.i = 0

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()


    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if player.y >= player.ground_y:
            player.i += 3
            t = player.i / 100
            player.y = (1 - t) * player.fall_calculate_list[1] + t * player.fall_calculate_list[2]
            player.x = (1 - t) * player.fall_calculate_list[0] + t * player.fall_calculate_list[0]
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
        else:
            player.In_Air = False
            player.cur_state = IdleState

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


next_state_table = {
    IdleState: {Right_UP: IdleState, Left_UP: IdleState, Right_DOWN: MoveState, Left_DOWN: MoveState,
                Air_DOWN: AirState, RAttack: IdleState, Up_DOWN: IdleState, Up_UP: IdleState},
    MoveState: {Right_UP: IdleState, Left_UP: IdleState, Left_DOWN: IdleState, Right_DOWN: IdleState,
                Air_DOWN: AirState, RAttack: MoveState, Up_DOWN: MoveState, Up_UP: MoveState},
    AirState: {Right_UP: AirState, Left_UP: AirState, Right_DOWN: AirMoveState, Left_DOWN: AirMoveState,
               Air_DOWN: FallingState, RAttack: AirState, Up_DOWN: AirMoveState},
    FallingState: {Right_DOWN: FallingState, Left_DOWN: FallingState, Right_UP: FallingState, Left_UP: FallingState,
                   Air_DOWN: AirState, RAttack: FallingState},
    AirMoveState: {Right_UP: AirMoveState, Left_UP: AirMoveState, Left_DOWN: AirMoveState, Right_DOWN: AirMoveState,
                   Up_DOWN: AirMoveState, Up_UP: AirState}
}


class Player:
    global first_floor_player_y

    def __init__(self):
        self.x, self.y = 100, first_floor_player_y  # 130은 지형의 높이.
        self.ground_y = self.y
        self.image = load_image('resource\\Character_sprite\\Player_animation.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.In_Air = False
        self.Rise_velocity = 0

    def add_event(self, event):
        self.event_que.insert(0, event)

    def MeleeAttack(self):
        pass

    def RangeAttack(self):
        print('test')
        Arrow = RangeAttack(self.x, self.y, self.dir * RangeAttack_speed_PPS * 10)
        game_world.add_object(Arrow, 1)
        print(RangeAttack_speed_PPS)

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
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event == Right_DOWN and not self.In_Air:
                self.velocity += Run_speed_PPS
            elif key_event == Left_DOWN and not self.In_Air:
                self.velocity -= Run_speed_PPS
            elif key_event == Right_UP and not self.In_Air:
                self.velocity -= Run_speed_PPS
            elif key_event == Left_UP and not self.In_Air:
                self.velocity += Run_speed_PPS
            elif key_event == Air_DOWN and not self.In_Air:
                self.y += 10
            elif key_event == Right_DOWN and self.In_Air:
                self.velocity += Air_speed_PPS
            elif key_event == Left_DOWN and self.In_Air:
                self.velocity -= Air_speed_PPS
            elif key_event == Right_UP and self.In_Air:
                self.velocity -= Air_speed_PPS
            elif key_event == Left_UP and self.In_Air:
                self.velocity += Air_speed_PPS
            elif key_event == Up_DOWN and self.In_Air:
                self.dir = 2
                self.Rise_velocity += Rise_speed_PPS
            elif key_event == Up_UP and self.In_Air:
                self.dir = 0
                self.Rise_velocity -= Rise_speed_PPS
            self.add_event(key_event)


class RangeAttack:
    global RangeAttack_speed_PPS

    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if RangeAttack.image == None:
            RangeAttack.image = load_image('resource\\RangeAttack.png')
        self.x, self.y, self.velocity = x, y, RangeAttack_speed_PPS

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
