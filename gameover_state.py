from pico2d import *

import game_framework
import title_state
import game_state

name = "GameOverState"
image = None
bgm = None


def enter():
    global image, bgm
    image = load_image('resource\\GameOver.png')
    bgm = load_music("resource\\Sound\\GameOver.mp3")
    bgm.set_volume(100)
    bgm.repeat_play()


def exit():
    global image, bgm
    del(image, bgm)


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
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
                game_framework.change_state(title_state)


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