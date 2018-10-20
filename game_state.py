from pico2d import *

import pause_state
import game_framework

name = 'GameState'

player = None
grass = None
font = None
move_direction = None


class Background:
    def __init__(self):
        self.image = load_image('resource\\Background\\d_grass.png')

    def draw(self):
        self.image.draw(250, 60)
        self.image.draw(500, 60)
        self.image.draw(750, 60)
        self.image.draw(1000, 60)

    def update(self):
        pass


class Player:
    def __init__(self):
        self.image = load_image('resource\\Character_sprite\\High_주인공.png')
        self.x, self.y = (100, 300)
        self.move_value = 0
        self.direction = 0

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        global move_direction

        if move_direction == 'right':
            self.move_value = 5
            self.x += self.move_value
            delay(0.05)
        elif move_direction == None:
            self.move_value = 0


"""
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
    global move_direction, key_release
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.push_state(pause_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            move_direction = 'right'
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            move_direction = None


def update():
    player.update()


def draw():
    clear_canvas()
    grass.draw()
    player.draw()
    update_canvas()