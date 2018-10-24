from pico2d import *


RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, JUMP_DOWN, JUMP_UP = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_x): JUMP_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_x): JUMP_UP
}


class IdleState:

    @staticmethod
    def enter(player):
        player.frame = 0
        player.timer = 1000

    @staticmethod
    def exit(player):
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
    def enter(player):
        player.frame = 0
        player.dir = player.velocity

    @staticmethod
    def exit(player):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.x += player.velocity
        player.x = clamp(25, player.x, 960 - 75)

    @staticmethod
    def draw(player):
        if player.velocity == 1:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
            delay(0.01)
        else:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
            delay(0.01)


class JumpUpState:

    @staticmethod
    def enter(player):
        player.frame = 0

    @staticmethod
    def exit(player):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        if player.velocity == 2:
            player.y += player.velocity
        else:
            player.y -= player.velocity

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)


class JumpDownState:

    @staticmethod
    def enter(player):
        player.frame = 0


    @staticmethod
    def exit(player):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        if player.velocity == 2 and player.y >= 280:  # 280은 지형의 높이.
            player.y -= player.velocity
        else:
            player.cur_state = IdleState

    @staticmethod
    def draw(player):
        if player.velocity == 2:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)
        else:
            player.image.clip_draw(player.frame * 150, 0, 150, 320, player.x, player.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                JUMP_DOWN: JumpUpState, JUMP_UP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState},
    JumpUpState: {JUMP_UP: JumpDownState, JUMP_DOWN: JumpUpState},
    JumpDownState: {JUMP_UP: JumpDownState, JUMP_DOWN: JumpDownState}
}
    
    
class Player:

    def __init__(self):
        self.x, self.y = 100, 280
        self.image = load_image('resource\\Character_sprite\\Player_animation.png')
        self.dir = 1
        self.velocity = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self)

    def change_state(self,  state):
        self.cur_state.exit(self)
        self.cur_state = state
        self.cur_state.enter(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.change_state(next_state_table[self.cur_state][event])

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
                self.velocity = 2
            elif key_event == JUMP_UP:
                self.velocity = 2
            self.add_event(key_event)