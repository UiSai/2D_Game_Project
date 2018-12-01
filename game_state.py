from pico2d import *

import pause_state
import gameover_state
import clear_state
import game_framework
import game_world

from player import Player
from en_mouse import Enemy_mouse
from en_cat import Enemy_cat
from en_boss import Enemy_boss
from stage1_BG import Background
# from item import *

name = 'GameState'

player = None
background = None
mouse = None
cat = None
boss = None
# item = None
font = None
move_direction = None
move_state = False
jump_state = False


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def enter():
    global player, background, mouse, cat, boss     # item

    player = Player()
    background = Background()
    mouse = Enemy_mouse()
    cat = Enemy_cat()
    boss = Enemy_boss()
    # item = Item_Health(200, 200)

    game_world.add_object(background, 0)
    game_world.add_object(player, 1)
    # game_world.add_object(item, 1)


def exit():
    game_world.clear()


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
    for game_object in game_world.all_objects():
        game_object.update()

    if not mouse.exist and background.block == 1:
        game_world.add_object(mouse, 1)

    if not cat.exist and background.block == 2:
        game_world.add_object(cat, 1)

    if mouse.exist and not player.Invincible_Status:
        if collide(player, mouse):
            if player.MAttack_Status:
                mouse.HP -= player.MA_Damage
            else:
                player.HP -= 1
                player.Invincible_Status = True

    if cat.exist and not player.Invincible_Status:
        if collide(player, cat):
            if player.MAttack_Status:
                cat.HP -= player.MA_Damage
            else:
                player.HP -= 1
                player.Invincible_Status = True

    if cat.magic.exist and not player.Invincible_Status:
        if collide(player, cat.magic):
            player.HP -= 1
            game_world.remove_object(cat.magic)
            player.Invincible_Status = True
            cat.magic.exist = False
        if cat.magic.shoot_dir == 0 and cat.magic.x <= cat.magic.target_x:
            game_world.remove_object(cat.magic)
            cat.magic.exist = False
        elif cat.magic.shoot_dir == 1 and cat.magic.x >= cat.magic.target_x:
            game_world.remove_object(cat.magic)
            cat.magic.exist = False

    if not boss.exist and not boss.dead and background.block == 6:
        game_world.add_object(boss, 1)

    if boss.exist and not player.Invincible_Status:
        if collide(player, boss):
            if player.MAttack_Status:
                boss.HP -= player.MA_Damage
            else:
                player.HP -= 1
                player.Invincible_Status = True

    if boss.knife.exist and not player.Invincible_Status:
        if collide(player, boss.knife):
            player.HP -= 1
            game_world.remove_object(boss.knife)
            player.Invincible_Status = True
            boss.knife.exist = False
        if boss.knife.shoot_dir == 0 and boss.knife.x <= boss.knife.target_x:
            game_world.remove_object(boss.knife)
            boss.knife.exist = False
        elif boss.knife.shoot_dir == 1 and boss.knife.x >= boss.knife.target_y:
            game_world.remove_object(boss.knife)
            boss.knife.exist = False

    """
    if item.exist:
        if collide(player, item):
            item.effect()
    """
    for i in range(10):
        if player.arrow[i].exist and mouse.HP > 0:
            if collide(player.arrow[i], mouse):
                mouse.HP -= player.RA_Damage
                player.arrow[i].exist = False
                player.arrow_num = clamp(0, i - 1, 9)
        if player.arrow[i].x < 25 or player.arrow[i].x > 1280 - 25:
            game_world.remove_object(player.arrow[i])
            player.arrow[i].exist = False
            player.arrow_num = i - 1
            player.arrow_num = clamp(0, i - 1, 9)

    if player.HP <= 0:
        game_framework.change_state(gameover_state)

    if background.block == 3 and player.y >= 940:
        background.block += 1
        player.y = 11
    elif background.block == 4 and player.y < 10:
        background.block -= 1
    elif background.block == 7:
        game_framework.change_state(clear_state)
    else:
        if player.x >= 1281:
            background.block += 1
            player.x = 2
        elif player.x <= -1:
            background.block -= 1
            player.x = 1278




def draw():
    global player

    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    player.health_point()

    update_canvas()