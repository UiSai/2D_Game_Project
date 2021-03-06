from pico2d import *
from arrow import RangeAttack
from stage1_BG import Background

import game_world
import game_framework
import game_state

first_floor_player_y = 200
Left, Right, Up, Fall, Neutral = 0, 1, 2, 3, 4

Pixel_per_Meter = 1 / 1.23  # 1픽셀에 1.23미터
Move_speed_MPS = 500
Move_speed_PPS = (Move_speed_MPS * Pixel_per_Meter)
Air_speed_MPS = 1000
Air_speed_PPS = (Air_speed_MPS * Pixel_per_Meter)
Rise_speed_PPS = (300 * Pixel_per_Meter)
Fall_speed_PPS = (1000 * Pixel_per_Meter)

Arrow_speed_MPS = 100
Arrow_speed_PPS = (Arrow_speed_MPS * Pixel_per_Meter)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

#background = Background()

Right_DOWN, Left_DOWN, Right_UP, Left_UP, Up_DOWN, Up_UP, Air_DOWN, MAttack, RAttack, Roll = range(10)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): Right_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): Left_DOWN,
    (SDL_KEYDOWN, SDLK_UP): Up_DOWN,
    (SDL_KEYDOWN, SDLK_a): Air_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): Right_UP,
    (SDL_KEYUP, SDLK_LEFT): Left_UP,
    (SDL_KEYUP, SDLK_UP): Up_UP,
    (SDL_KEYDOWN, SDLK_z): MAttack,
    (SDL_KEYDOWN, SDLK_x): RAttack,
    (SDL_KEYDOWN, SDLK_s): Roll
}


"""
class IdleState:

    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.velocity += Move_speed_PPS
        elif event == Left_DOWN:
            player.velocity -= Move_speed_PPS
        elif event == Right_UP:
            player.velocity -= Move_speed_PPS
        elif event == Left_UP:
            player.velocity += Move_speed_PPS
        elif event == Air_DOWN:
            player.y += 10

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        if player.dir == Right:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 61, 0, 61, 130, player.x, player.y)
"""


class GroundState:

    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.dir = Right
            # player.Move_Status = True
            player.velocity = Move_speed_PPS
        elif event == Left_DOWN:
            player.dir = Left
            # player.Move_Status = True
            player.velocity = -Move_speed_PPS
        elif event == Right_UP and player.dir == Right:
            player.velocity = 0
        elif event == Left_UP and player.dir == Left:
            player.velocity = 0
        if event == Air_DOWN:
            player.y += 10
        elif event == Roll:
            player.Invincible_Status = True

    """
    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.dir = Right
            player.velocity += Move_speed_PPS
        elif event == Left_DOWN:
            player.dir = Left
            player.velocity -= Move_speed_PPS
        elif event == Right_UP:
            player.velocity -= Move_speed_PPS
        elif event == Left_UP:
            player.velocity += Move_speed_PPS
        if event == Air_DOWN:
            player.y += 10
        elif event == MAttack:
            player.MeleeAttack()
            player.MAttack_Status = True
    """

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()
        elif event == MAttack:
            player.MeleeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.velocity * game_framework.frame_time
        if game_state.background.block == 4 and player.x < 600:
            player.cur_state = FallingState

        player.clamp_and_timer()

    @staticmethod
    def draw(player):
        if not player.MAttack_Status:
            if player.velocity > 0:
                player.image.clip_draw(int(player.frame) * 250, 500, 250, 250, player.x, player.y)  # 걷기 오른쪽 이동
            elif player.velocity < 0:
                player.image.clip_draw(int(player.frame) * 250, 750, 250, 250, player.x, player.y)  # 걷기 왼쪽 이동
            else:
                if player.dir == Right:
                    player.image.clip_draw(int(player.frame) * 250, 0, 250, 250, player.x, player.y)  # 오른쪽을 보고 서있다
                elif player.dir == Left:
                    player.image.clip_draw(int(player.frame) * 250, 250, 250, 250, player.x, player.y)  # 왼쪽을 보고 서있다
        else:
            if player.dir == Left:
                    player.image.clip_draw(int(player.frame) * 250, 1250, 250, 250, player.x, player.y)  # 왼쪽 공격
            else:
                    player.image.clip_draw(int(player.frame) * 250, 1000, 250, 250, player.x, player.y)  # 오른쪽 공격


class AirState:
    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.dir = Right
            player.velocity = Air_speed_PPS
        elif event == Left_DOWN:
            player.dir = Left
            player.velocity = -Air_speed_PPS
        elif event == Right_UP and player.dir == Right:
            player.velocity = 0
        elif event == Left_UP and player.dir == Left:
            player.velocity = 0
        if event == Up_DOWN:
            player.Rise_velocity = Rise_speed_PPS
        elif event == Up_UP:
            player.Rise_velocity = 0
    """
    @staticmethod
    def enter(player, event):
        if event == Right_DOWN:
            player.velocity += Air_speed_PPS
        elif event == Left_DOWN:
            player.velocity -= Air_speed_PPS
        elif event == Right_UP:
            player.velocity -= Air_speed_PPS
        elif event == Left_UP:
            player.velocity += Air_speed_PPS
        elif event == Air_DOWN:
            if not player.velocity == 0:
                player.velocity = 0
        if event == Up_DOWN:
            player.Rise_velocity += Rise_speed_PPS
        elif event == Up_UP:
            player.Rise_velocity -= Rise_speed_PPS
    """
    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()
        elif event == MAttack:
            player.MeleeAttack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.velocity * game_framework.frame_time
        player.y += player.Rise_velocity * game_framework.frame_time

        player.clamp_and_timer()

    @staticmethod
    def draw(player):
        if not player.MAttack_Status:
            if player.velocity < 0:
                player.dir = Left
                player.image.clip_draw(int(player.frame) * 250, 2750, 250, 250, player.x, player.y)  # 공중 왼쪽 이동
            elif player.velocity > 0:
                player.dir = Right
                player.image.clip_draw(int(player.frame) * 250, 2500, 250, 250, player.x, player.y)  # 공중 오른쪽 이동
            else:
                if player.Rise_velocity > 0:
                    if player.dir == Left:
                        player.image.clip_draw(int(player.frame) * 250, 2250, 250, 250, player.x, player.y)  # 왼쪽을 보는 상승
                    elif player.dir == Right:
                        player.image.clip_draw(int(player.frame) * 250, 2000, 250, 250, player.x, player.y)  # 오른쪽을 보는 상승
                else:
                    if player.dir == Left:
                        player.image.clip_draw(int(player.frame) * 250, 1750, 250, 250, player.x, player.y)  # 왼쪽을 보고 서있다
                    elif player.dir == Right:
                        player.image.clip_draw(int(player.frame) * 250, 1500, 250, 250, player.x, player.y)  # 오른쪽을 보고 서있다
        else:
            if player.dir == Left:
                    player.image.clip_draw(int(player.frame) * 250, 1250, 250, 250, player.x, player.y)  # 왼쪽 공격
            else:
                    player.image.clip_draw(int(player.frame) * 250, 1000, 250, 250, player.x, player.y)  # 오른쪽 공격


class FallingState:

    @staticmethod
    def enter(player, event):
        player.Falling_velocity = Fall_speed_PPS * game_framework.frame_time
        if event == Right_DOWN:
            player.dir = Right
            player.velocity = Move_speed_PPS
        elif event == Left_DOWN:
            player.dir = Left
            player.velocity = -Move_speed_PPS
        elif event == Right_UP and player.dir == Right:
            if not player.velocity == 0:
                player.velocity = 0
        elif event == Left_UP and player.dir == Left:
            if not player.velocity == 0:
                player.velocity = 0

    @staticmethod
    def exit(player, event):
        if event == RAttack:
            player.RangeAttack()
        elif event == MAttack:
            player.MeleeAttack()

    @staticmethod
    def do(player):
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.Falling_velocity
        if player.y <= player.ground_y and not game_state.background.block == 4:
            player.cur_state = GroundState
        else:
            player.clamp_and_timer()


    @staticmethod
    def draw(player):
        if not player.MAttack_Status:
            if player.dir == Right:
                player.image.clip_draw(int(player.frame) * 250, 0, 250, 250, player.x, player.y)  # 오른쪽 낙하
            else:
                player.image.clip_draw(int(player.frame) * 250, 250, 250, 250, player.x, player.y)  # 왼쪽 낙하
        else:
            if player.dir == Left:
                    player.image.clip_draw(int(player.frame) * 250, 1250, 250, 250, player.x, player.y)  # 왼쪽 공격
            else:
                    player.image.clip_draw(int(player.frame) * 250, 1000, 250, 250, player.x, player.y)  # 오른쪽 공격


next_state_table = {
    GroundState: {Right_UP: GroundState, Left_UP: GroundState, Left_DOWN: GroundState, Right_DOWN: GroundState,
                  Air_DOWN: AirState, MAttack: GroundState, RAttack: GroundState, Up_DOWN: GroundState,
                  Up_UP: GroundState, Roll: GroundState},
    AirState: {Right_UP: AirState, Left_UP: AirState, Right_DOWN: AirState, Left_DOWN: AirState,
               Air_DOWN: FallingState, RAttack: AirState, Up_DOWN: AirState, Up_UP: AirState, MAttack: AirState,
               Roll: AirState},
    FallingState: {Right_DOWN: FallingState, Left_DOWN: FallingState, Right_UP: FallingState, Left_UP: FallingState,
                   Air_DOWN: AirState, RAttack: FallingState, Up_DOWN: FallingState, Up_UP: FallingState,
                   MAttack: FallingState, Roll: FallingState}
}


class Player:
    def __init__(self):
        self.x, self.y = 100, first_floor_player_y  # 130은 지형의 높이
        self.ground_y = self.y
        self.image = load_image('resource\\Character_sprite\\Player_animation.png')
        self.hhealth_image = load_image('resource\\Half_HP.png')
        self.health_image = load_image('resource\\HP.png')
        self.dir = Right
        self.HP = 6
        self.MA_Damage = 5
        self.RA_Damage = 1
        self.velocity = 0
        self.Rise_velocity = 0
        self.Falling_velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = GroundState
        self.cur_state.enter(self, None)
        self.In_Air = False
        self.arrow = [RangeAttack(self.x, self.y) for i in range(10)]
        self.arrow_num = 0
        self.Move_Status = False
        self.MAttack_Status = False
        self.Invincible_Status = False
        self.MeleeTimer = 0
        self.Invincible_Timer = 0
        self.Falling_stop_judge = False

    def add_event(self, event):
        self.event_que.insert(0, event)

    def MeleeAttack(self):
        self.MAttack_Status = True

    def RangeAttack(self):
        for i in range(10):
            if not self.arrow[i].exist:
                self.arrow[i].exist = True
                self.arrow[i].x, self.arrow[i].y = self.x, self.y
                self.arrow[i].dir = self.dir

                self.arrow_num = clamp(0, i, 9)
                game_world.add_object(self.arrow[i], 2)
                break

    def get_bb(self):
        if self.MAttack_Status:
            if self.dir == Right:
                return self.x - 37, self.y - 125, self.x + 70, self.y + 100
            else:
                return self.x - 70, self.y - 125, self.x + 37, self.y + 100
        else:
            return self.x - 37, self.y - 125, self.x + 37, self.y + 100

    def update(self):
        self.cur_state.do(self)
        # print(self.cur_state)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        # draw_rectangle(*self.get_bb())

    def clamp_and_timer(self):
        if game_state.background.block == 3:
            self.x = clamp(-10, self.x, 600)
            self.y = clamp(self.ground_y, self.y, 970)
        elif game_state.background.block == 4:
            self.y = clamp(0, self.y, 880)
            self.x = clamp(50, self.x, 1290)
            if self.y < self.ground_y:
                if self.x <= 600:
                    self.x = clamp(50, self.x, 600)
                else:
                    pass
                    self.x = clamp(50, self.x, 600)
                    # self.y = clamp(self.ground_y, self.y, 880)
        elif game_state.background.block == 6 and game_state.boss.exist:
            self.x = clamp(50, self.x, 1250)
            self.y = clamp(self.ground_y, self.y, 880)
        elif game_state.background.block == 6 and not game_state.boss.exist:
            self.x = clamp(50, self.x, 1290)
            self.y = clamp(self.ground_y, self.y, 880)
        elif game_state.background.block == 1:
            self.x = clamp(50, self.x, 1290)
            self.y = clamp(self.ground_y - 1, self.y, 880)
        else:
            self.x = clamp(-10, self.x, 1290)
            self.y = clamp(self.ground_y, self.y, 880)

        # if game_state.background.block == 1:

        """
        if not game_state.background.block == 3:
            self.y = clamp(self.ground_y, self.y, 900)
        
        if game_state.background.block == 1:
            self.x = clamp(25, self.x, 1290)
        elif game_state.background.block == 3:
            self.x = clamp(-10, self.x, 1230)
        """
        if self.MAttack_Status:
            self.MeleeTimer += game_framework.frame_time
            if self.MeleeTimer >= 0.4:
                self.MAttack_Status = False
                self.MeleeTimer = 0

        if self.Invincible_Status:
            self.Invincible_Timer += game_framework.frame_time
            if self.Invincible_Timer >= 2:
                self.Invincible_Status = False
                self.Invincible_Timer = 0

    def health_point(self):
        if self.HP >= 1:
            self.hhealth_image.draw(50, 920)
            if self.HP >= 2:
                self.health_image.draw(50, 920)
                if self.HP >= 3:
                    self.hhealth_image.draw(100, 920)
                    if self.HP >= 4:
                        self.health_image.draw(100, 920)
                        if self.HP >= 5:
                            self.hhealth_image.draw(150, 920)
                            if self.HP >= 6:
                                self.health_image.draw(150, 920)

    def input_buttons(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


