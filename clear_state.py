from pico2d import *

import game_framework
import title_state
import game_state

name = "ClearState"
image = None
bgm = None
staff = None
timer = 0
roll_enable = False

def enter():
    global image, bgm, staff
    image = load_image('resource\\clear.png')
    staff = load_image('resource\\StaffRoll.png')
    bgm = load_music("resource\\Sound\\clear.mp3")
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
                game_framework.change_state(title_state)


def draw():
    global roll_enable

    if not roll_enable:
        clear_canvas()
        image.draw(640, 480)
        update_canvas()
    else:
        clear_canvas()
        staff.draw(640, 480)
        update_canvas()


def update():
    global timer, roll_enable

    timer += game_framework.frame_time
    if timer >= 5:
        timer = 0
        roll_enable = True



def pause():
    pass


def resume():
    pass