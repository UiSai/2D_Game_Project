from pico2d import *

import datetime
import game_world

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, JUMP_DOWN, JUMP_UP = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_x): JUMP_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_x): JUMP_UP,
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
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
            delay(0.1)
        else:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
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
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
            delay(0.01)
        else:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)  # 왼쪽 이동 스프라이트
            delay(0.01)


class JumpState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.jump_height = 100
        player.jump_height_list = [player.y, player.y + player.jump_height]
        player.jumping = False
        player.i = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        """
        if player.velocity == 2:
            player.y += player.velocity
        else:
            player.y -= player.velocity
        """
        if player.y <= player.ground_y + player.jump_height:
            player.i += 3
            t = player.i / 100
            player.y = (1 - t) * player.jump_height_list[0] + t * player.jump_height_list[1]
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
        else:
            player.jumping is True
            player.add_event(5)

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)  # 왼쪽 스프라이트


class FallingState:

    @staticmethod
    def enter(player, event):
        player.frame = 0
        player.jump_height_list = [player.y, player.ground_y]
        player.i = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        """
        if player.velocity == 2 and player.y >= 280:  # 280은 지형의 높이.
            player.y -= player.velocity
        else:
            player.cur_state = IdleState
        """
        if player.y >= player.ground_y:
            player.i += 3
            t = player.i / 100
            player.y = (1 - t) * player.jump_height_list[0] + t * player.jump_height_list[1]
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
        else:
            player.jumping is False
            player.cur_state = IdleState

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)  # 왼쪽 스프라이트


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                JUMP_DOWN: JumpState, JUMP_UP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               JUMP_DOWN: JumpState, JUMP_UP: RunState},
    JumpState: {JUMP_DOWN: JumpState, JUMP_UP: FallingState},
    FallingState: {JUMP_DOWN: FallingState, JUMP_UP: FallingState}
}


class Player:

    def __init__(self):
        self.x, self.y = 100, 280
        self.ground_y = self.y
        self.image = load_image('resource\\Character_sprite\\Player_animation.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.jumping = False
        self.jump_height = 500
        self.jump_height_list = []
        self.testlist = [1]

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
                self.velocity += 1
            elif key_event == LEFT_DOWN:
                self.velocity -= 1
            elif key_event == RIGHT_UP:
                self.velocity -= 1
            elif key_event == LEFT_UP:
                self.velocity += 1
            elif key_event == JUMP_DOWN:
                self.velocity += 5
            elif key_event == JUMP_UP:
                self.velocity -= 5
            self.add_event(key_event)

