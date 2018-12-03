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
from item import Item_Health

name = 'GameState'

player = None
background = None
mouse = None
cat = None
boss = None
item = None
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
    global player, background, mouse, cat, boss, item

    player = Player()
    background = Background()
    mouse = Enemy_mouse()
    cat = Enemy_cat()
    boss = Enemy_boss()
    item = Item_Health(640, 150)

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

    print(player.velocity)
    if not mouse.exist and background.block == 1:
        game_world.add_object(mouse, 1)

    if not cat.exist and background.block == 2:
        game_world.add_object(cat, 1)

    if not item.exist and background.block == 5:
        game_world.add_object(item, 1)

    if mouse.exist:
        if collide(player, mouse):
            if player.MAttack_Status and not mouse.Invincible_Status:
                mouse.HP -= player.MA_Damage
                mouse.Invincible_Status = True
            elif not player.Invincible_Status:
                player.HP -= 1
                player.Invincible_Status = True

    if cat.exist:
        if collide(player, cat):
            if player.MAttack_Status and not cat.Invincible_Status:
                cat.HP -= player.MA_Damage
            elif not player.Invincible_Status:
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

    if boss.exist:
        if collide(player, boss):
            if player.MAttack_Status and not boss.Invincible_Status:
                boss.HP -= player.MA_Damage
            elif not player.Invincible_Status:
                player.HP -= 1
                player.Invincible_Status = True

    # if boss.knife.exist and not player.Invincible_Status:
#    if not player.Invincible_Status:
#        if collide(player, boss.knife):
#            player.HP -= 1
#            game_world.remove_object(boss.knife)
#            player.Invincible_Status = True
#            boss.knife.exist = False
#        if boss.knife.shoot_dir == 0 and boss.knife.x <= boss.knife.target_x:
#            game_world.remove_object(boss.knife)
#            boss.knife.exist = False
#        elif boss.knife.shoot_dir == 1 and boss.knife.x >= boss.knife.target_y:
#            game_world.remove_object(boss.knife)
#            boss.knife.exist = False

    if item.exist and background.block == 5:
        if collide(player, item):
            if player.HP < 6:
                player.HP = 6
                item.HP -= 1



    for i in range(10):
        if boss.knife[i].exist and player.HP > 0 and not player.Invincible_Status:
            if collide(boss.knife[i], player):
                game_world.remove_object(boss.knife[i])
                player.HP -= boss.damage
                boss.knife[i].exist = False
                boss.arrow_num = clamp(0, i - 1, 9)
        if boss.knife[i].y < 0 or boss.knife[i].y > 961 or boss.knife[i].x < 0 or boss.knife[i].x > 1280:
            game_world.remove_object(boss.knife[i])
            boss.knife[i].exist = False
            boss.knife_num = i - 1
            boss.arrow_num = clamp(0, i - 1, 9)
            #boss.add_event(0)


    """
    if item.exist:
        if collide(player, item):
            item.effect()
    """
    for i in range(10):
        if player.arrow[i].exist and mouse.HP > 0 and background.block == 1:
            if collide(player.arrow[i], mouse):
                game_world.remove_object(player.arrow[i])
                mouse.HP -= player.RA_Damage
                player.arrow[i].exist = False
                player.arrow_num = clamp(0, i - 1, 9)
        elif player.arrow[i].exist and cat.HP > 0 and background.block == 2:
            if collide(player.arrow[i], cat):
                game_world.remove_object(player.arrow[i])
                cat.HP -= player.RA_Damage
                player.arrow[i].exist = False
                player.arrow_num = clamp(0, i - 1, 9)
        if player.arrow[i].exist and boss.HP > 0 and background.block == 6:
            if collide(player.arrow[i], boss):
                game_world.remove_object(player.arrow[i])
                boss.HP -= player.RA_Damage
                player.arrow[i].exist = False
                player.arrow_num = clamp(0, i - 1, 9)
        if player.arrow[i].x < 25 or player.arrow[i].x > 1280 - 25:
            game_world.remove_object(player.arrow[i])
            player.arrow[i].exist = False
            player.arrow_num = i - 1
            player.arrow_num = clamp(0, i - 1, 9)

    if player.HP <= 0:
        game_framework.change_state(gameover_state)

    if background.block == 3 and player.y >= 955:
        background.block += 1
        player.y = 11
        for i in range(10):
            player.arrow[i].exist = False
        game_world.remove_object_in_layer(2)
    elif background.block == 4 and player.y < 10:
        background.block -= 1
        player.y = 950
        for i in range(10):
            player.arrow[i].exist = False
        game_world.remove_object_in_layer(2)
    elif background.block == 7:
        game_framework.change_state(clear_state)
    else:
        if player.x >= 1281:
            background.block += 1
            player.x = 2
            for i in range(10):
                player.arrow[i].exist = False
            game_world.remove_object_in_layer(2)
        elif player.x <= -1:
            background.block -= 1
            player.x = 1278
            for i in range(10):
                player.arrow[i].exist = False
            game_world.remove_object_in_layer(2)


def draw():
    global player

    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    player.health_point()

    update_canvas()