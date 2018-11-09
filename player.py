from pico2d import *
#from temp_rangeattack import RangeAttack

import game_world

first_floor_player_y = 130

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Run_speed_MPS = 5
Run_speed_PPS = (Run_speed_MPS * Pixel_per_Meter)
Air_speed_MPS = 10
Air_speed_PPS = (Air_speed_MPS * Pixel_per_Meter)
RangeAttack_speed_MPS = 15
RangeAttack_speed_PPS = (RangeAttack_speed_MPS * Pixel_per_Meter)


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
        player.timer = 1000

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8

    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
            delay(0.1)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
            delay(0.1)


class MoveState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.dir = player.velocity

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.x += player.velocity
        player.x = clamp(25, player.x, 960)

    @staticmethod
    def draw(player):
        if player.velocity == Run_speed_PPS:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 걷기 오른쪽 이동
            delay(0.01)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 걷기 왼쪽 이동
            delay(0.01)


class AirState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.In_Air = True

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8

    @staticmethod
    def draw(player):
        if player.dir == 1:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


class AirMoveState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.dir = player.velocity

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.x += player.velocity
        player.x = clamp(25, player.x, 960)

    @staticmethod
    def draw(player):
        if player.velocity > Air_speed_PPS:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 공중 오른쪽 이동
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 공중 왼쪽 이동


class FallingState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.fall_calculate_list = [player.x, player.y, player.ground_y]
        player.i = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        if player.y >= player.ground_y:
            player.i += 3
            t = player.i / 100
            player.y = (1 - t) * player.fall_calculate_list[1] + t * player.fall_calculate_list[2]
            player.x = (1 - t) * player.fall_calculate_list[0] + t * player.fall_calculate_list[0]
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.In_Air = False
            player.cur_state = IdleState

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


next_state_table = {
    IdleState: {Right_UP: IdleState, Left_UP: IdleState, Right_DOWN: MoveState, Left_DOWN: MoveState,
                Air_DOWN: AirState, RAttack: IdleState},
    MoveState: {Right_UP: IdleState, Left_UP: IdleState, Left_DOWN: IdleState, Right_DOWN: IdleState,
                Air_DOWN: AirState},
    AirState: {Right_UP: AirState, Left_UP: AirState, Right_DOWN: AirMoveState, Left_DOWN: AirMoveState,
               Air_DOWN: FallingState},
    FallingState: {Right_DOWN: FallingState, Left_DOWN: FallingState, Right_UP: FallingState, Left_UP: FallingState,
                   Air_DOWN: AirState},
    AirMoveState: {Right_UP: AirState, Left_UP: AirState, Left_DOWN: AirMoveState, Right_DOWN: AirMoveState,
                   Air_DOWN: FallingState}
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
            if key_event == Right_DOWN:
                self.velocity += Run_speed_PPS
            elif key_event == Left_DOWN:
                self.velocity -= Run_speed_PPS
            elif key_event == Right_UP:
                self.velocity -= Run_speed_PPS
            elif key_event == Left_UP:
                self.velocity += Run_speed_PPS
            elif key_event == Air_DOWN and self.cur_state == IdleState:
                self.y += 10
            elif key_event == Right_DOWN and self.cur_state == AirState:
                self.velocity += Air_speed_PPS
            elif key_event == Left_DOWN and self.cur_state == AirState:
                self.velocity -= Air_speed_PPS
            elif key_event == Right_UP and self.cur_state == AirState:
                self.velocity -= Air_speed_PPS
            elif key_event == Left_UP and self.cur_state == AirState:
                self.velocity += Air_speed_PPS
            self.add_event(key_event)


class RangeAttack:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if RangeAttack.image == None:
            RangeAttack.image = load_image('resource\\RangeAttack.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
