from pico2d import *

import pause_state
import game_framework

name = 'GameState'

player = None
grass = None
font = None
move_direction = None
move_state = False
jump_state = False


class Background:
    def __init__(self):
        self.image = load_image('resource\\Background\\d_grass.png')
        self.first_floor = 60

    def draw(self):
        self.image.draw(250, self.first_floor)
        self.image.draw(500, self.first_floor)
        self.image.draw(750, self.first_floor)
        self.image.draw(1000, self.first_floor)

    def update(self):
        pass


class Player:
    def __init__(self):
        self.x, self.y = (100, 280)
        self.move_value = 0
        self.direction = 0
        self.image = load_image('resource\\Character_sprite\\High_주인공.png')
        self.jump_height = self.y

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        global move_direction, jump_state

        if move_direction == 'right':
            self.move_value = 1
            self.x += self.move_value
        elif move_direction is None:
            self.move_value = 0  # 이동속도
        elif move_direction == 'left':
            self.move_value = 1
            self.x -= self.move_value
        elif move_direction == 'jump':
            self.move_value = 1
            if self.y - 160 < self.jump_height and jump_state is True:
                self.y += self.move_value
            elif self.y - 160 == self.jump_height and jump_state is True:
                jump_state = False
                self.y -= self.move_value
            elif grass.first_floor + 60 < self.y - 160 <= self.jump_height and jump_state is False:
                self.y -= self.move_value


"""
                elif self.y - 160 > self.jump_height:
                    self.y -= self.move_value
class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.x >= 800:
            self.dir = -1
        elif self.x <= 0:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
"""


def enter():
    global player, grass

    player = Player()
    grass = Background()


def exit():
    global player, grass

    del (player)
    del (grass)


def pause():
    pass


def resume():
    pass


def input_buttons():
    global move_direction, move_state, jump_state

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.push_state(pause_state)  # 여기까지 시스템
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            move_direction = 'right'
            move_state = True  # 필요없지만 혹시 모르니 남겨둔다
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT and move_direction == 'right':
            move_direction = None
            move_state = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            move_direction = 'left'
            move_state = True
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT and move_direction == 'left':
            move_direction = None
            move_state = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x and move_direction != 'jump':
            move_direction = 'jump'
            jump_state = True


def update():
    player.update()


def draw():
    clear_canvas()
    grass.draw()
    player.draw()
    update_canvas()