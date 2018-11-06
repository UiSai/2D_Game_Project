from pico2d import *

import game_world


Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Run_speed_MPS = 5
Run_speed_PPS = (Run_speed_MPS * Pixel_per_Meter)
Jump_speed_MPS = 1
Jump_speed_PPS = (Jump_speed_MPS * Pixel_per_Meter)


RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, JUMP_DOWN, JUMP_UP, JUMPR_DOWN, JUMPL_DOWN, JUMPR_UP, JUMPL_UP = range(10)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_x): JUMP_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_x): JUMP_UP,
    (SDL_KEYDOWN, SDLK_s): JUMPL_DOWN,
    (SDL_KEYDOWN, SDLK_d): JUMPR_DOWN,
    (SDL_KEYUP, SDLK_s): JUMPL_UP,
    (SDL_KEYUP, SDLK_d): JUMPR_UP
}


class IdleState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.timer = 1000

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
            delay(0.1)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
            delay(0.1)


class RunState:

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
        if player.velocity == 1:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
            delay(0.01)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 이동 스프라이트
            delay(0.01)


class JumpState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.jump_max_height = 100
        player.jump_height_list = [player.y, player.y + player.jump_max_height]
        player.jumping_x = [player.x, player.x]
        player.jumping = False
        player.i = 0

    @staticmethod
    def exit(player, event):
        if event == RIGHT_DOWN:
            player.x_in_jumping += 3

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        if player.y <= player.ground_y + player.jump_max_height:
            player.i += 3
            t = player.i / 100
            player.y = (1 - t) * player.jump_height_list[0] + t * player.jump_height_list[1]
            player.x = (1 - t) * player.jumping_x[0] + t * player.jumping_x[1]
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.jumping is True
            player.add_event(5)

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


class JumpLState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.jump_max_height = 100
        player.jump_height_list = [player.y, player.y + player.jump_max_height]
        player.jumping_x = [player.x, player.x - player.jump_max_height]
        player.jumping = False
        player.i = 0

    @staticmethod
    def exit(player, event):
        if event == RIGHT_DOWN:
            player.x_in_jumping += 3

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        if player.y <= player.ground_y + player.jump_max_height:
            player.i += 3
            t = player.i / 100
            player.y = (1 - t) * player.jump_height_list[0] + t * player.jump_height_list[1]
            player.x = (1 - t) * player.jumping_x[0] + t * player.jumping_x[1]
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.jumping is True
            player.add_event(1)

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


class JumpRState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.jump_max_height = 100
        player.jump_height_list = [player.y, player.y + player.jump_max_height]
        player.jumping_x = [player.x, player.x + player.jump_max_height]
        player.jumping = False
        player.i = 0

    @staticmethod
    def exit(player, event):
        if event == RIGHT_DOWN:
            player.x_in_jumping += 3

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        if player.y <= player.ground_y + player.jump_max_height:
            player.i += 3
            t = player.i / 100
            player.y = (1 - t) * player.jump_height_list[0] + t * player.jump_height_list[1]
            player.x = (1 - t) * player.jumping_x[0] + t * player.jumping_x[1]
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.jumping is True
            player.add_event(1)

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


class FallingState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.jump_height_list = [player.y, player.ground_y]
        player.jumping_x = [player.x, player.x]
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
            player.y = (1 - t) * player.jump_height_list[0] + t * player.jump_height_list[1]
            player.x = (1 - t) * player.jumping_x[0] + t * player.jumping_x[1]
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.jumping is False
            player.cur_state = IdleState

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 61, 0, 61, 130, player.x, player.y)  # 왼쪽 스프라이트


next_state_table = {
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                JUMP_DOWN: JumpState, JUMP_UP: IdleState, JUMPL_DOWN: JumpLState, JUMPR_DOWN: JumpRState,
                JUMPL_UP: IdleState, JUMPR_UP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               JUMP_DOWN: JumpState, JUMP_UP: RunState, JUMPL_DOWN: JumpLState, JUMPR_DOWN: JumpRState,
               JUMPL_UP: IdleState, JUMPR_UP: IdleState},
    JumpState: {JUMP_DOWN: JumpState, JUMP_UP: FallingState, RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState,
                RIGHT_UP: JumpState, LEFT_UP: JumpState},
    JumpRState: {JUMPR_DOWN: JumpRState, JUMPR_UP: FallingState, RIGHT_DOWN: JumpRState, LEFT_DOWN: JumpRState,
                 RIGHT_UP: JumpRState, LEFT_UP: JumpRState},
    JumpLState: {JUMPL_DOWN: JumpLState, JUMPL_UP: FallingState, RIGHT_DOWN: JumpLState, LEFT_DOWN: JumpLState,
                 RIGHT_UP: JumpLState, LEFT_UP: JumpLState},
    FallingState: {JUMP_DOWN: FallingState, JUMP_UP: FallingState, RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState,
                   RIGHT_UP: JumpState, LEFT_UP: JumpState}
}


class Player:

    def __init__(self):
        self.x, self.y = 100, 130  # 130은 지형의 높이.
        self.ground_y = self.y
        self.image = load_image('resource\\Character_sprite\\Player_animation.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.jumping = False
        self.jump_max_height = 500
        self.jump_height_list = []
        self.x_in_jumping = self.x

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
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event == RIGHT_DOWN:
                self.velocity += Run_speed_PPS
            elif key_event == LEFT_DOWN:
                self.velocity -= Run_speed_PPS
            elif key_event == RIGHT_UP:
                self.velocity -= Run_speed_PPS
            elif key_event == LEFT_UP:
                self.velocity += Run_speed_PPS
            elif key_event == JUMP_DOWN:
                self.velocity += Jump_speed_PPS
            elif key_event == JUMP_UP:
                self.velocity -= Jump_speed_PPS
            self.add_event(key_event)

