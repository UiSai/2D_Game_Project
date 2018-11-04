from pico2d import *

import pause_state
import game_framework

from player import Player
from enemy import Enemy

name = 'GameState'

player = None
grass = None
font = None
move_direction = None
move_state = False
jump_state = False
enemy = None


class Background:
    def __init__(self):
        self.image = load_image('resource\\Background\\d_grass.png')
        self.first_floor = 40

    def draw(self):
        self.image.draw(150, self.first_floor)
        self.image.draw(450, self.first_floor)
        self.image.draw(700, self.first_floor)
        self.image.draw(950, self.first_floor)
        self.image.draw(1200, self.first_floor)

    def update(self):
        pass

"""
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
            elif grass.first_floor + 60 < self.y - 160 < self.jump_height and jump_state is False:
                self.y -= self.move_value
            elif self.y - 160 == self.jump_height and jump_state is False:
                move_direction = None
        elif move_direction == 'right_jump':
            self.move_value = 1
            self.x += self.move_value
            self.y += self.move_value
"""


def enter():
    global player, grass, enemy

    player = Player()
    grass = Background()
    enemy = Enemy()


def exit():
    global player, grass, enemy

    del (player)
    del (grass)
    del (enemy)


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
        else:
            player.input_buttons(event)


def update():
    player.update()
    print(player.cur_state)


def draw():
    clear_canvas()
    grass.draw()
    player.draw()
    enemy.draw()
    update_canvas()

    """
    elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
        move_direction = 'right'
        move_state = True  # 필요없지만 혹시 모르니 남겨둔다
        if jump_state is True and move_state is True:
            move_direction = 'right_jump'
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
        jump_state = True  # 일반적 이동
    """