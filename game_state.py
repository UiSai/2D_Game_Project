from pico2d import *

import pause_state
import game_framework

name = 'GameState'

class Main_character:
    def __init__(self):
        self.image = load_image('H:\\2DGP\\2D_Game_Project\\resource\\Character_sprite\\High_주인공.png')
        self.x, self.y = (100, 60)

    def draw(self):
        self.image.draw(100, 60)

    def move_right(self):
        self.image.draw()

def input_button():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_state(pause_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:

def right_move():
    pass

open_canvas()

character = Main_character()

running = True

while running:
    input_button()

    character.draw()

    update_canvas()

close_canvas()