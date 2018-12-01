import game_framework
from pico2d import *
import title_state


open_canvas(1280, 960, sync=True)
game_framework.run(title_state)

close_canvas()