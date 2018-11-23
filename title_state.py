from pico2d import *

import game_framework
import game_state

name = "TitleState"
image = None


def enter():
    global image
    image = load_image('resource\\Title.png')
    easter = False
    easter_commend = []


def exit():
    global image
    del(image)


def input_buttons():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
                game_framework.change_state(game_state)


def draw():
    clear_canvas()
    image.draw(640, 480)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass