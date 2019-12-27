import sys
import pygame
import traceback
import os
import hero
import enemy
import pickle
import block
import widget
import supply
from pygame.locals import *
from random import choice

pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (140, 100)

bg_size = width, height = 1100, 600
screen = pygame.display.set_mode(bg_size, DOUBLEBUF, 32)
pygame.display.set_caption('丛林反腐大冒险——侯亮平')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 200, 220)
ORANGE = (255, 168, 0)
RED = (255, 0, 0)
TEXT_COLOR = (235, 127, 0)

# 读取历史最高分
read_score_file = open('record.pkl', 'rb')
record_score = pickle.load(read_score_file)
read_score_file.close()

# icon
icon = pygame.image.load('src/icon/life.png').convert_alpha()
pygame.display.set_icon(icon)

# 加载声音
pygame.mixer.music.load('src/sounds/backgroundmusic.ogg')
pygame.mixer.music.set_volume(0.2)
button_sound = pygame.mixer.Sound('src/sounds/button.wav')
button_sound.set_volume(0.6)
begin_sound = pygame.mixer.Sound('src/sounds/begin_music.wav')
begin_sound.set_volume(0.8)
gameover_sound = pygame.mixer.Sound('src/sounds/gameover.wav')
gameover_sound.set_volume(0.6)
running_sound = pygame.mixer.Sound('src/sounds/running.wav')
running_sound.set_volume(0.8)
upgrade_sound = pygame.mixer.Sound('src/sounds/upgrade.wav')
upgrade_sound.set_volume(0.9)
supply_sound = pygame.mixer.Sound('src/sounds/supply.wav')
supply_sound.set_volume(0.6)
get_supply_sound = pygame.mixer.Sound('src/sounds/get_supply.wav')
get_supply_sound.set_volume(1.0)
become_inv = pygame.mixer.Sound('src/sounds/invincible.wav')
become_inv.set_volume(0.6)
reward = pygame.mixer.Sound('src/sounds/reward.wav')
reward.set_volume(0.3)
gameover_sound = pygame.mixer.Sound('src/sounds/gameover.wav')
gameover_sound.set_volume(0.6)

# 控件类图片
sound_on = pygame.image.load('src/image/widgets/sound_on.png').convert_alpha()
sound_off = pygame.image.load('src/image/widgets/sound_off.png').convert_alpha()
pause_img = pygame.image.load('src/image/widgets/unpause.png').convert_alpha()
unpause_img = pygame.image.load('src/image/widgets/pause.png').convert_alpha()
back_img = pygame.image.load('src/image/widgets/back.png').convert_alpha()
gameover_up = pygame.image.load('src/image/widgets/up.png').convert_alpha()
gameover_down = pygame.image.load('src/image/widgets/down.png').convert_alpha()
up_rect = gameover_up.get_rect()
down_rect = gameover_down.get_rect()
up_rect.left, up_rect.top = 0, -300
down_rect.left, down_rect.top = 0, 600

start = pygame.image.load('src/image/widgets/start.png').convert_alpha()
start_unpressed = pygame.image.load('src/image/widgets/start.png').convert_alpha()
start_pressed = pygame.image.load('src/image/widgets/start_pressed.png').convert_alpha()
instruction = pygame.image.load('src/image/widgets/instruction.png').convert_alpha()
instruction_unpressed = pygame.image.load('src/image/widgets/instruction.png').convert_alpha()
instruction_pressed = pygame.image.load('src/image/widgets/instruction_pressed.png').convert_alpha()
game_exit = pygame.image.load('src/image/widgets/exit.png').convert_alpha()
exit_unpressed = pygame.image.load('src/image/widgets/exit.png').convert_alpha()
exit_pressed = pygame.image.load('src/image/widgets/exit_pressed.png').convert_alpha()
score_reset = pygame.image.load('src/image/widgets/reset.png').convert_alpha()
reset_unpressed = pygame.image.load('src/image/widgets/reset.png').convert_alpha()
reset_pressed = pygame.image.load('src/image/widgets/reset_pressed.png').convert_alpha()
instr = pygame.image.load('src/image/widgets/instr.png').convert_alpha()
instr_rect = instr.get_rect()
start_rect = start.get_rect()
exit_rect = game_exit.get_rect()
reset_rect = score_reset.get_rect()
instruction_rect = instruction.get_rect()
start_rect.right, start_rect.top = -138, 220
instruction_rect.right, instruction_rect.top = -6, 220
reset_rect.left, reset_rect.top = 1106, 220
exit_rect.left, exit_rect.top = 1238, 220
instr_rect.left, instr_rect.bottom = 250, 0

# 标题
title_imgs = [pygame.image.load('src/image/widgets/title/1.png').convert_alpha(),
              pygame.image.load('src/image/widgets/title/2.png').convert_alpha(),
              pygame.image.load('src/image/widgets/title/3.png').convert_alpha(),
              pygame.image.load('src/image/widgets/title/4.png').convert_alpha(),
              pygame.image.load('src/image/widgets/title/5.png').convert_alpha(),
              pygame.image.load('src/image/widgets/title/6.png').convert_alpha(),
              pygame.image.load('src/image/widgets/title/7.png').convert_alpha(),
              pygame.image.load('src/image/widgets/title/8.png').convert_alpha()]
title = widget.Widget(bg_size, title_imgs, (250, 0))

# 静态障碍图片
stone_img = pygame.image.load('src/image/block/stone.png').convert_alpha()
box_img = pygame.image.load('src/image/block/box.png').convert_alpha()
tong_img = pygame.image.load('src/image/block/tong.png').convert_alpha()
# 静态障碍爆炸图片
des_stone = [pygame.image.load('src/image/source/boom_stone/1.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/2.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/3.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/4.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/5.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/6.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/7.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/8.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/9.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/10.png').convert_alpha(),
             pygame.image.load('src/image/source/boom_stone/11.png').convert_alpha()]
des_tong = [pygame.image.load('src/image/source/boom_tong/1.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/2.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/3.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/4.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/5.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/6.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/7.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/8.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/9.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/10.png').convert_alpha(),
            pygame.image.load('src/image/source/boom_tong/11.png').convert_alpha()]
des_box = [pygame.image.load('src/image/source/boom_box/1.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/2.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/3.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/4.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/5.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/6.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/7.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/8.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/9.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/10.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/11.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_box/12.png').convert_alpha()]

# 子弹图片
bullet_img = pygame.image.load('src/image/block/bullet.png').convert_alpha()
# 子弹摧毁
des_bullet = [pygame.image.load('src/image/source/boom/1.png').convert_alpha(),
              pygame.image.load('src/image/source/boom/2.png').convert_alpha(),
              pygame.image.load('src/image/source/boom/3.png').convert_alpha(),
              pygame.image.load('src/image/source/boom/4.png').convert_alpha(),
              pygame.image.load('src/image/source/boom/5.png').convert_alpha(),
              pygame.image.load('src/image/source/boom/6.png').convert_alpha(),
              pygame.image.load('src/image/source/boom/7.png').convert_alpha()]

# 动态障碍图片

# 小车图片
car_img = [pygame.image.load('src/image/block/car/1.png').convert_alpha(),
           pygame.image.load('src/image/block/car/2.png').convert_alpha(),
           pygame.image.load('src/image/block/car/3.png').convert_alpha(),
           pygame.image.load('src/image/block/car/4.png').convert_alpha(),
           pygame.image.load('src/image/block/car/5.png').convert_alpha(),
           pygame.image.load('src/image/block/car/6.png').convert_alpha()]
#小车爆炸图片
des_car = [pygame.image.load('src/image/source/boom_car/1.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/2.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/3.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/4.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/5.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/6.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/7.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/8.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/9.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/10.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/11.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/12.png').convert_alpha(),
           pygame.image.load('src/image/source/boom_car/13.png').convert_alpha()]

# 滚石图片
rolling_img = [pygame.image.load('src/image/block/rolling_stone/1.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/2.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/3.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/4.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/5.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/6.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/7.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/8.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/9.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/10.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/11.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/12.png').convert_alpha(),
               pygame.image.load('src/image/block/rolling_stone/13.png').convert_alpha()]
# 滚石爆炸图片
des_rolling = [pygame.image.load('src/image/source/boom_rolling/1.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/2.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/3.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/4.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/5.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/6.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/7.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/8.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/9.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/10.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/11.png').convert_alpha(),
               pygame.image.load('src/image/source/boom_rolling/12.png').convert_alpha()]

# 狼图片
wolf_img = [pygame.image.load('src/image/block/wolf/1.png').convert_alpha(),
            pygame.image.load('src/image/block/wolf/2.png').convert_alpha(),
            pygame.image.load('src/image/block/wolf/3.png').convert_alpha(),
            pygame.image.load('src/image/block/wolf/4.png').convert_alpha(),
            pygame.image.load('src/image/block/wolf/5.png').convert_alpha(),
            pygame.image.load('src/image/block/wolf/6.png').convert_alpha(),
            pygame.image.load('src/image/block/wolf/7.png').convert_alpha(),
            pygame.image.load('src/image/block/wolf/8.png').convert_alpha()]
# 狼死亡图片
des_wolf = [pygame.image.load('src/image/source/wolfdie/death1.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death2.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death3.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death4.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death5.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death6.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death7.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death8.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death9.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death10.png').convert_alpha(),
            pygame.image.load('src/image/source/wolfdie/death11.png').convert_alpha()]

# 敌人图片
# 贪官图片
tanguan_img = [pygame.image.load('src/image/enemy/tanguan/1.png').convert_alpha(),
               pygame.image.load('src/image/enemy/tanguan/2.png').convert_alpha(),
               pygame.image.load('src/image/enemy/tanguan/3.png').convert_alpha(),
               pygame.image.load('src/image/enemy/tanguan/4.png').convert_alpha(),
               pygame.image.load('src/image/enemy/tanguan/5.png').convert_alpha(),
               pygame.image.load('src/image/enemy/tanguan/6.png').convert_alpha(),
               pygame.image.load('src/image/enemy/tanguan/7.png').convert_alpha(),
               pygame.image.load('src/image/enemy/tanguan/8.png').convert_alpha(),
               pygame.image.load('src/image/enemy/tanguan/9.png').convert_alpha()]
des_tanguan = [pygame.image.load('src/image/source/des_gaoyuliang/1.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/2.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/3.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/4.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/5.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/6.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/7.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/8.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/9.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/10.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/11.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/12.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/13.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/14.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/15.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/16.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/17.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/18.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/18.png').convert_alpha(),
               pygame.image.load('src/image/source/des_gaoyuliang/20.png').convert_alpha()]

# 赵瑞龙图片
zhaoruilong_img = [pygame.image.load('src/image/enemy/zhaoruilong2/1.png').convert_alpha(),
                   pygame.image.load('src/image/enemy/zhaoruilong2/2.png').convert_alpha(),
                   pygame.image.load('src/image/enemy/zhaoruilong2/3.png').convert_alpha(),
                   pygame.image.load('src/image/enemy/zhaoruilong2/4.png').convert_alpha(),
                   pygame.image.load('src/image/enemy/zhaoruilong2/5.png').convert_alpha(),
                   pygame.image.load('src/image/enemy/zhaoruilong2/6.png').convert_alpha()]
des_zhao = [pygame.image.load('src/image/source/des_zhao/1.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/2.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/3.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/4.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/5.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/6.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/7.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/8.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/9.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/10.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/11.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/12.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/13.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/14.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/15.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/16.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/17.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/18.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/19.png').convert_alpha(),
            pygame.image.load('src/image/source/des_zhao/20.png').convert_alpha()]

# 祁同伟图片
qi_img = [pygame.image.load('src/image/enemy/qi/1.png').convert_alpha(),
          pygame.image.load('src/image/enemy/qi/2.png').convert_alpha(),
          pygame.image.load('src/image/enemy/qi/3.png').convert_alpha(),
          pygame.image.load('src/image/enemy/qi/4.png').convert_alpha(),
          pygame.image.load('src/image/enemy/qi/5.png').convert_alpha(),
          pygame.image.load('src/image/enemy/qi/6.png').convert_alpha(),
          pygame.image.load('src/image/enemy/qi/7.png').convert_alpha()]
des_qito = [pygame.image.load('src/image/source/des_qi/1.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/2.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/3.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/4.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/5.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/6.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/7.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/8.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/9.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/10.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/11.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/12.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/13.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/14.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/15.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/16.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/17.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/18.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/19.png').convert_alpha(),
            pygame.image.load('src/image/source/des_qi/20.png').convert_alpha()]

# 高小琴图片
gx_img = [pygame.image.load('src/image/enemy/gaoxiaoqin/1.png').convert_alpha(),
          pygame.image.load('src/image/enemy/gaoxiaoqin/2.png').convert_alpha(),
          pygame.image.load('src/image/enemy/gaoxiaoqin/3.png').convert_alpha(),
          pygame.image.load('src/image/enemy/gaoxiaoqin/4.png').convert_alpha(),
          pygame.image.load('src/image/enemy/gaoxiaoqin/5.png').convert_alpha(),
          pygame.image.load('src/image/enemy/gaoxiaoqin/6.png').convert_alpha(),
          pygame.image.load('src/image/enemy/gaoxiaoqin/7.png').convert_alpha()]
des_gxqi = [pygame.image.load('src/image/source/des_gxq/1.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/2.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/3.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/4.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/5.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/6.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/7.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/8.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/9.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/10.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/11.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/12.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/13.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/14.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/15.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/16.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/17.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/18.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/19.png').convert_alpha(),
            pygame.image.load('src/image/source/des_gxq/20.png').convert_alpha()]

background1 = pygame.image.load('src/image/source/background.png').convert_alpha()
background2 = pygame.image.load('src/image/source/background.png').convert_alpha()
gameover_img = pygame.image.load('src/image/widgets/gameover.png').convert_alpha()
background1_rect = background1.get_rect()
background2_rect = background2.get_rect()
gameover_rect = gameover_img.get_rect()
background1_rect.left, background1_rect.top = 0, 0
background2_rect.left, background2_rect.top = bg_size[0] - 1, 0
gameover_rect.left, gameover_rect.bottom = 250, 0

# 静态障碍
stone = block.StaticBlock(bg_size, stone_img, des_stone)
box = block.StaticBlock(bg_size, box_img, des_box)
tong = block.StaticBlock(bg_size, tong_img, des_tong)
stone.des_sound = pygame.mixer.Sound('src/sounds/stone_down.wav')
box.des_sound = pygame.mixer.Sound('src/sounds/tong_down.wav')
tong.des_sound = pygame.mixer.Sound('src/sounds/tong_down.wav')
stone.des_sound.set_volume(1.0)
box.des_sound.set_volume(1.0)
tong.des_sound.set_volume(1.0)
staticBlock = []
staticBlock.append(stone)
staticBlock.append(tong)
staticBlock.append(box)

# 动态障碍
car = block.DynamicBlock(bg_size, car_img, 10, 6, 400, des_car)
rolling = block.DynamicBlock(bg_size, rolling_img, 8, 13, 400, des_rolling)
wolf = block.DynamicBlock(bg_size, wolf_img, 7, 8, 400, des_wolf)
car.des_sound = pygame.mixer.Sound('src/sounds/dynamic_dowm.wav')
rolling.des_sound = pygame.mixer.Sound('src/sounds/dynamic_dowm.wav')
wolf.des_sound = pygame.mixer.Sound('src/sounds/wolfdie.wav')
car.des_sound.set_volume(1.0)
rolling.des_sound.set_volume(1.0)
wolf.des_sound.set_volume(1.0)
dynamicDlocks = []
dynamicDlocks.append(car)
dynamicDlocks.append(rolling)
dynamicDlocks.append(wolf)

# 敌人的集合列表
#gaoxiaoqin = enemy.Enemy(bg_size, gx_img, des_gxqi, "GXQ")
zhaoruilong = enemy.Enemy(bg_size, zhaoruilong_img, des_zhao, "ZRL")
qitongwei = enemy.Enemy(bg_size, qi_img, des_qito, "QTW")
gaoyuliang = enemy.Enemy(bg_size, tanguan_img, des_tanguan, "GYL")
enemies = []
#enemies.append(gaoxiaoqin)
enemies.append(zhaoruilong)
enemies.append(gaoyuliang)
enemies.append(qitongwei)

# 控件类实例化
sound = widget.Button(bg_size, sound_on, (1042, -8))
pause = widget.Button(bg_size, pause_img, (984, -8))
back = widget.Button(bg_size, back_img, (926, -8))

# 补给类实例化
angel_img = pygame.image.load('src/image/supply/angel.png').convert_alpha()
angry_img = pygame.image.load('src/image/supply/angel_angry.png').convert_alpha()
ball_img = pygame.image.load('src/image/supply/ball.png').convert_alpha()
heart_img = pygame.image.load('src/image/supply/heart.png').convert_alpha()
angel = supply.Angel(bg_size, angel_img)
ball = supply.Supply(bg_size, ball_img)
heart = supply.Supply(bg_size, heart_img)
supplies = [ball, heart]

# 重置控件的位置以及状态
def reset_global():
    global start,start_rect,instruction,instruction_rect,reset_rect,exit_rect

    start_rect.right, start_rect.top = -138, 220
    instruction_rect.right, instruction_rect.top = -6, 220
    reset_rect.left, reset_rect.top = 1106, 220
    exit_rect.left, exit_rect.top = 1238, 220
    start = start_unpressed
    instruction = instruction_unpressed
    title.reset()
    pause.reset()
    sound.reset()
    back.reset()
    angel.reset()

# 主运行函数
def main():
    global sound,pause,back,record_score

    # 创建敌人
    mysupply = choice(supplies)
    bullet = block.Bullet(bg_size, bullet_img, des_bullet)
    myhero = hero.Hero(bg_size)
    myenemy = choice(enemies)
    mystaticblock = choice(staticBlock)
    mydynamicblock = choice(dynamicDlocks)
    # 创建敌人精灵组
    all_enemies = pygame.sprite.Group()
    all_enemies.add(bullet)
    all_enemies.add(myenemy)
    all_enemies.add(mystaticblock)
    all_enemies.add(mydynamicblock)

    # 重置所有精灵的位置和状态
    for e in enemies:
        e.reset()
    for e in staticBlock:
        e.reset()
    for e in dynamicDlocks:
        e.reset()
    for s in supplies:
        s.reset()

    # 更新画面用于延迟
    delay = 100
    # 绘制的帧数，表示第几帧
    hero_index = 0
    enemy_index = 0
    # 二段跳的数值
    jump_flag = 0
    # 生命
    life_image = pygame.image.load('src/image/source/life/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_rect.top = 728
    life_num = 3
    # 道具
    ball_rect = ball_img.get_rect()
    ball_rect.left, ball_rect.top = 10, 600
    ball_font = pygame.font.Font('src/font/MAIAN.TTF', 48)
    ball_num = 3
    ball_text = ball_font.render('× %d' % ball_num, True, WHITE)
    ball_text_rect = ball_text.get_rect()
    ball_text_rect.left, ball_text_rect.top = 20 + ball_rect.width, 600
    # 补给计数
    supply_count = 0
    supply_update_num = 2500
    # 等级
    level = 0
    # 判断是否已读取文件
    recorded = False
    # 主角无敌的标志
    invincible_event = False
    # 启动main函数的标志
    ball_begin_flag = True
    # 暂停的标志
    pause_flag = False
    # 各个等级的标志
    bullet_flag = False
    static_flag = False
    dynamic_flag = False
    # 显示提示的标志
    show_talk = False
    # 无敌还原的标志
    uninvincible = False
    # 升级的标志
    level_tip = False
    # 放走贪官的标志
    letgo_flag = False
    # 主角重生事件
    REBORN_TIMER = USEREVENT
    # 主角无敌事件
    INVINCIBLE_TIMER = USEREVENT + 1
    # 显示提示事件
    TALK_TIMER = USEREVENT + 2
    # 非无敌事件
    UNINVINCIBLE_TIMER = USEREVENT + 3
    # 升级奖励事件
    LEVEL_TIMER = USEREVENT + 4
    # 画线的宽度增量
    line_width = 1
    # 画线的宽度
    line = 1
    # 统计放走的贪官数
    letgo_count = 0
    # 捉住的贪官数
    get_count = 0
    # 分数
    score = 0
    # 增加的分数
    plus = 0
    # 增加的分数的中间的变量
    plus_temp = 0
    # 增加的分数格式化
    plus_str = '+%d'
    # 增加的分数的字体颜色
    plus_color = ORANGE
    # 游戏的帧数
    FPS = 90

    # 各种障碍爆炸图片的帧数，表示第几帧
    static_destroy_index = 0
    enemy_destroy_index = 0
    dynamic_destroy_index = 0
    bullet_index = 0

    # 分数文字
    score_font = pygame.font.Font('src/font/MAIAN.TTF', 36)
    score_text = score_font.render('Score : %d' % score, True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.left, score_rect.top = 10, -50

    # 对话
    talk_font = pygame.font.Font('src/font/STXINWEI.TTF', 30)
    text_list = ['给你送补给啦~', '么么哒~', '小心呐~', '给你个大宝贝~']
    text = choice(text_list)
    talk_text = talk_font.render(text, True, WHITE)

    # 陈海天使的警告
    worn_font = pygame.font.Font('src/font/STXINWEI.TTF', 30)
    worn = '你怎么把腐败分子给放了？！！'
    worn_text = worn_font.render(worn, True, RED)
    worn_rect = worn_text.get_rect()

    # 游戏是否正在运行
    running = True
    # 每一帧的时间间隔
    clock = pygame.time.Clock()

    # 声音的标志
    if sound.flag:
        reward.set_volume(0)
        become_inv.set_volume(0)
        get_supply_sound.set_volume(0)
        supply_sound.set_volume(0)
        car.des_sound.set_volume(0)
        for e in enemies:
            e.des_sound.set_volume(0)
        rolling.des_sound.set_volume(0)
        wolf.des_sound.set_volume(0)
        stone.des_sound.set_volume(0)
        box.des_sound.set_volume(0)
        tong.des_sound.set_volume(0)
        begin_sound.set_volume(0)
        myhero.hurt_sound.set_volume(0)
        myhero.music.set_volume(0)
        running_sound.set_volume(0)
        myhero.music.set_volume(0)
        upgrade_sound.set_volume(0)
        pygame.mixer.music.pause()
    else:
        reward.set_volume(0.3)
        become_inv.set_volume(0.6)
        supply_sound.set_volume(0.6)
        get_supply_sound.set_volume(1.0)
        car.des_sound.set_volume(1.0)
        for e in enemies:
            e.des_sound.set_volume(0.6)
        rolling.des_sound.set_volume(1.0)
        wolf.des_sound.set_volume(1.0)
        stone.des_sound.set_volume(1.0)
        box.des_sound.set_volume(1.0)
        tong.des_sound.set_volume(1.0)
        begin_sound.set_volume(0.8)
        myhero.hurt_sound.set_volume(0.8)
        myhero.music.set_volume(0.8)
        running_sound.set_volume(1.0)
        myhero.music.set_volume(0.8)
        upgrade_sound.set_volume(0.9)
        pygame.mixer.music.unpause()

    # 游戏主循环
    while running:
        # 事件处理
        for event in pygame.event.get():
            # 退出程序
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                # 方向键向上跳起
                if (event.key == K_UP) and (jump_flag != 2):
                    if jump_flag == 1:
                        myhero.resetSpeed()
                        myhero.music_flag = True
                    jump_flag += 1
                    # 方向键向左用道具
                elif event.key == K_LEFT:
                    if ball_num > 0:
                        become_inv.play()
                        ball_num -= 1
                        myhero.invincible = True
                        pygame.time.set_timer(INVINCIBLE_TIMER, 10000)
                        pygame.time.set_timer(UNINVINCIBLE_TIMER, 7000)
                        invincible_event = True
                        uninvincible = False

            if event.type == MOUSEBUTTONUP:
                # 点击暂停按钮
                if event.button == 1 and pause.rect.collidepoint(event.pos):
                    if pause_flag:
                        if not sound.flag:
                            running_sound.set_volume(1.0)
                            become_inv.set_volume(0.6)
                        else:
                            running_sound.set_volume(0)
                            become_inv.set_volume(0)
                        pause.image = pause_img
                        pause_flag = not pause_flag
                    else:
                        pause.image = unpause_img
                        become_inv.set_volume(0)
                        running_sound.set_volume(0)
                        pause_flag = not pause_flag
                # 点击返回按钮
                elif event.button == 1 and back.rect.collidepoint(event.pos):
                    reward.set_volume(0)
                    become_inv.set_volume(0)
                    get_supply_sound.set_volume(0)
                    supply_sound.set_volume(0)
                    car.des_sound.set_volume(0)
                    for e in enemies:
                        e.des_sound.set_volume(0)
                    rolling.des_sound.set_volume(0)
                    wolf.des_sound.set_volume(0)
                    stone.des_sound.set_volume(0)
                    box.des_sound.set_volume(0)
                    tong.des_sound.set_volume(0)
                    begin_sound.set_volume(0)
                    myhero.hurt_sound.set_volume(0)
                    myhero.music.set_volume(0)
                    running_sound.stop()
                    myhero.music.set_volume(0)
                    upgrade_sound.set_volume(0)
                    pygame.mixer.music.pause()
                    screen_shot = screen.subsurface((0, 0, width, height)).copy()
                    door_close(screen_shot)
                # 点击声音按钮
                elif event.button == 1 and sound.rect.collidepoint(event.pos):
                    if not sound.flag:
                        reward.set_volume(0)
                        become_inv.set_volume(0)
                        get_supply_sound.set_volume(0)
                        supply_sound.set_volume(0)
                        car.des_sound.set_volume(0)
                        for e in enemies:
                            e.des_sound.set_volume(0)
                        rolling.des_sound.set_volume(0)
                        wolf.des_sound.set_volume(0)
                        stone.des_sound.set_volume(0)
                        box.des_sound.set_volume(0)
                        tong.des_sound.set_volume(0)
                        begin_sound.set_volume(0)
                        myhero.hurt_sound.set_volume(0)
                        myhero.music.set_volume(0)
                        running_sound.set_volume(0)
                        myhero.music.set_volume(0)
                        upgrade_sound.set_volume(0)
                        pygame.mixer.music.pause()
                        sound.image = sound_off
                    else:
                        reward.set_volume(0.3)
                        become_inv.set_volume(0.6)
                        supply_sound.set_volume(0.6)
                        get_supply_sound.set_volume(1.0)
                        car.des_sound.set_volume(1.0)
                        for e in enemies:
                            e.des_sound.set_volume(0.6)
                        rolling.des_sound.set_volume(1.0)
                        wolf.des_sound.set_volume(1.0)
                        stone.des_sound.set_volume(1.0)
                        box.des_sound.set_volume(1.0)
                        tong.des_sound.set_volume(1.0)
                        begin_sound.set_volume(0.8)
                        myhero.hurt_sound.set_volume(0.8)
                        myhero.music.set_volume(0.8)
                        running_sound.set_volume(1.0)
                        myhero.music.set_volume(0.8)
                        upgrade_sound.set_volume(0.9)
                        pygame.mixer.music.unpause()
                        sound.image = sound_on
                    sound.flag = not sound.flag
            # 主角重生事件处理
            if event.type == REBORN_TIMER:
                myhero.active = True
                if not invincible_event:
                    myhero.reset()
            # 主角无敌事件处理
            if event.type == INVINCIBLE_TIMER:
                myhero.invincible = False
                invincible_event = False
                myhero.uninvincible = False
                uninvincible = False
                pygame.time.set_timer(INVINCIBLE_TIMER, 0)
            # 主角非无敌事件处理
            if event.type == UNINVINCIBLE_TIMER:
                uninvincible = True
                pygame.time.set_timer(UNINVINCIBLE_TIMER, 0)
            # 等级提升事件处理
            if event.type == LEVEL_TIMER:
                show_talk = False
            # 天使提示事件处理
            if event.type == TALK_TIMER:
                show_talk = False

        # 判断是否升级的条件
        if level == 0 and score >= 10000:
            upgrade_sound.play()
            supply_update_num = 2000
            if supply_count > supply_update_num:
                supply_count = supply_update_num - 100
            static_flag = True
            level = 1
            level_tip = True
        elif level == 1 and score >= 150000:
            upgrade_sound.play()
            supply_update_num = 1600
            if supply_count > supply_update_num:
                supply_count = supply_update_num - 100
            dynamic_flag = True
            level = 2
            level_tip = True
        elif level == 2 and score >= 300000:
            supply_update_num = 1400
            if supply_count > supply_update_num:
                supply_count = supply_update_num - 100
            upgrade_sound.play()
            bullet_flag = True
            level = 3
            level_tip = True

        # 判断是否暂停
        if not pause_flag:
            # 绘制场景
            screen.blit(background1, background1_rect)
            screen.blit(background2, background2_rect)

            # 背景移动
            background1_rect.left -= 4
            background2_rect.left -= 4
            if background1_rect.left <= -1100:
                background1_rect.left = 0
                background2_rect.left = bg_size[0] - 1

            # 敌人名称
            myenemy.name_rect.right = myenemy.rect.right
            screen.blit(myenemy.name, myenemy.name_rect)

            # 绘制炮弹提示线段
            if bullet_flag:
                if bullet.active:
                    if 1100 < bullet.rect.left < 3000:
                        line_flag = True
                    else:
                        line_flag = False
                        line = 1
                    if line_flag:
                        pygame.draw.line(screen, RED, (0, bullet.rect.centery), bullet.rect.center, line)
                        if not (delay % 3):
                            line += line_width
                        if (line == 1):
                            line_width = 1
                        if (line == 5):
                            line_width = -1

            # 绘制静态障碍
            if static_flag:
                if mystaticblock.active:
                    mystaticblock.move()
                    screen.blit(mystaticblock.image, mystaticblock.rect)
                    # 判断静态障碍是否不在窗口范围
                    if (mystaticblock.rect.right < myhero.rect.left + 30) and (myhero.active) and (mystaticblock.away):
                        score += 1000
                        plus += 1000
                        mystaticblock.away = False
                    if mystaticblock.rect.right < 0:
                        all_enemies.remove(mystaticblock)
                        mystaticblock.reset()
                        mystaticblock = choice(staticBlock)
                        all_enemies.add(mystaticblock)
                else:
                    # 毁灭
                    mystaticblock.move()
                    if (not (delay % 4)):
                        if static_destroy_index == 0:
                            mystaticblock.des_sound.play()
                            score += 1000
                            plus += 1000
                        screen.blit(mystaticblock.destroy_imgs[static_destroy_index], mystaticblock.rect)
                        static_destroy_index = (static_destroy_index + 1) % len(mystaticblock.destroy_imgs)
                        if static_destroy_index == 0:
                            all_enemies.remove(mystaticblock)
                            mystaticblock.reset()
                            mystaticblock = choice(staticBlock)
                            all_enemies.add(mystaticblock)

            # 绘制敌人
            if (not (delay % 4)):
                enemy_index = (enemy_index + 1) % len(myenemy.images)
                myenemy.image = myenemy.images[enemy_index]
            if myenemy.active:
                myenemy.move()
                screen.blit(myenemy.image, myenemy.rect)
                # 判断敌人是否不在窗口范围
                if (myenemy.rect.right < 0):
                    letgo_flag = True
                    letgo_count += 1
                    score -= 10000
                    plus -= 10000
                    all_enemies.remove(myenemy)
                    myenemy.reset()
                    myenemy = choice(enemies)
                    all_enemies.add(myenemy)
            else:
                # 毁灭
                letgo_flag = False
                get_count += 1
                myenemy.move()
                if (not (delay % 5)):
                    if enemy_destroy_index == 0:
                        myenemy.speed = 4
                        myenemy.des_sound.play()
                        score += 6000
                        plus += 6000
                    enemy_destroy_index = (enemy_destroy_index + 1) % len(myenemy.destroy_imgs)
                    if enemy_destroy_index == 0:
                        all_enemies.remove(myenemy)
                        myenemy.reset()
                        myenemy = choice(enemies)
                        all_enemies.add(myenemy)
                screen.blit(myenemy.destroy_imgs[enemy_destroy_index], myenemy.rect)

            # 绘制动态障碍
            if dynamic_flag:
                if (not (delay % 3)):
                    mydynamicblock.block_index = (mydynamicblock.block_index + 1) % mydynamicblock.index
                    mydynamicblock.image = mydynamicblock.images[mydynamicblock.block_index]
                    mydynamicblock.setMask()
                if mydynamicblock.active:
                    mydynamicblock.move()
                    screen.blit(mydynamicblock.image, mydynamicblock.rect)
                    # 判断动态障碍是否不在窗口范围
                    if (mydynamicblock.rect.right < myhero.rect.left + 30) and (myhero.active) and (mydynamicblock.away):
                        score += 2500
                        plus += 2500
                        mydynamicblock.away = False
                    if mydynamicblock.rect.right < 0:
                        all_enemies.remove(mydynamicblock)
                        mydynamicblock.reset()
                        mydynamicblock = choice(dynamicDlocks)
                        all_enemies.add(mydynamicblock)
                else:
                    # 毁灭
                    mydynamicblock.move()
                    if (not (delay % 6)):
                        if dynamic_destroy_index == 0:
                            mydynamicblock.speed = 4
                            mydynamicblock.des_sound.play()
                            score += 2500
                            plus += 2500
                        dynamic_destroy_index = (dynamic_destroy_index + 1) % len(mydynamicblock.destroy_imgs)
                        if dynamic_destroy_index == 0:
                            all_enemies.remove(mydynamicblock)
                            mydynamicblock.reset()
                            mydynamicblock = choice(dynamicDlocks)
                            all_enemies.add(mydynamicblock)
                        if mydynamicblock != wolf:
                            screen.blit(mydynamicblock.destroy_imgs[dynamic_destroy_index], mydynamicblock.rect)
                    if mydynamicblock == wolf:
                        image = mydynamicblock.destroy_imgs[dynamic_destroy_index]
                        wolf_rect = image.get_rect()
                        wolf_rect.right, wolf_rect.bottom = mydynamicblock.rect.right, mydynamicblock.rect.bottom
                        screen.blit(image, wolf_rect)

            # 角色跳起
            if not (delay % 2):
                if jump_flag:
                    running_sound.stop()
                    myhero.jump()
                    if invincible_event:
                        if uninvincible:
                            if myhero.uninvincible:
                                myhero.image = myhero.images[10]
                            else:
                                myhero.image = myhero.inv_imgs[10]
                            if (not (delay % 3)):
                                myhero.uninvincible = not myhero.uninvincible
                        else:
                            myhero.image = myhero.inv_imgs[10]
                    else:
                        myhero.image = myhero.images[10]
                    myhero.setMask(10)
                    if myhero.rect.bottom > 400:
                        running_sound.play(-1)
                        myhero.music_flag = True
                        myhero.resetSpeed()
                        myhero.resetPos()
                        jump_flag = 0

            # 绘制炮弹
            if bullet_flag:
                if bullet.active:
                    bullet.move()
                    screen.blit(bullet.image, bullet.rect)
                    # 判断子弹是否不在窗口范围
                    if (bullet.rect.right < myhero.rect.left + 30) and (myhero.active) and (bullet.away):
                        score += 4000
                        plus += 4000
                        bullet.away = False
                    if bullet.rect.right < 0:
                        bullet.reset()
                        line_width = 1
                else:
                    if (not (delay % 5)):
                        if bullet_index == 0:
                            if not sound.flag:
                                bullet.des_sound.play()
                            score += 4000
                            plus += 4000
                        bullet_index = (bullet_index + 1) % len(bullet.destroy_imgs)
                        if bullet_index == 0:
                            bullet.reset()
                            line_width = 1
                        image = bullet.destroy_imgs[bullet_index]
                        new_rect = image.get_rect()
                        new_rect.center = bullet.rect.center
                        screen.blit(image, new_rect)

            # 绘制天使
            if not(delay % 2):
                angel.move()
            screen.blit(angel.image, angel.rect)

            # 绘制对话
            if letgo_flag:
                angel.image = angry_img
                worn_rect.right, worn_rect.top = angel.rect.left, 40
                screen.blit(worn_text, worn_rect)
            else:
                angel.image = angel_img
                if level_tip:
                    level_tip = False
                    text = '腐败分子变得更狡猾啦！'
                    pygame.time.set_timer(LEVEL_TIMER, 5000)
                    COLOR = ORANGE
                    talk_text = talk_font.render(text, True, COLOR)
                    show_talk = True
                    supply_count = 0
                    mysupply.active = True
                else:
                    if supply_count == supply_update_num - 100:
                        pygame.time.set_timer(TALK_TIMER, 5000)
                        text = choice(text_list)
                        COLOR = WHITE
                        talk_text = talk_font.render(text, True, COLOR)
                        show_talk = True
                if show_talk:
                    text_rect = talk_text.get_rect()
                    text_rect.right, text_rect.top = angel.rect.left - 20, 55
                    screen.blit(talk_text, text_rect)

            # 绘制补给
            if supply_count == supply_update_num:
                supply_sound.play()
                supply_count = 0
                mysupply.active  = True
            if mysupply.active:
                mysupply.move()
                screen.blit(mysupply.image, mysupply.rect)
                if mysupply.rect.right < 0:
                    mysupply.active = False
                    mysupply.reset()
                    mysupply = choice(supplies)
                # 检测主角是否获得补给
                if pygame.sprite.collide_mask(myhero, mysupply):
                    get_supply_sound.play()
                    if mysupply == ball:
                        ball_num += 1
                    elif mysupply == heart:
                        life_num += 1
                        if life_num > 8:
                            life_num = 8
                    mysupply.reset()
                    mysupply = choice(supplies)

            # 角色移动
            if (not (delay % 4)) and (not jump_flag):
                hero_index = (hero_index + 1) % 12
                if invincible_event:
                    if uninvincible:
                        if myhero.uninvincible:
                            myhero.image = myhero.images[hero_index]
                        else:
                            myhero.image = myhero.inv_imgs[hero_index]
                        if (not (delay % 3)):
                            myhero.uninvincible = not myhero.uninvincible
                    else:
                        myhero.image = myhero.inv_imgs[hero_index]
                else:
                    myhero.image = myhero.images[hero_index]
                myhero.setMask(hero_index)

            # 绘制主角
            if not myhero.active:
                if not myhero.switch_img:
                    screen.blit(myhero.image, myhero.rect)
                myhero.switch_img = not myhero.switch_img
            else:
                screen.blit(myhero.image, myhero.rect)

            # 绘制道具数量
            ball_text = ball_font.render('× %d' % ball_num, True, WHITE)
            if ball_begin_flag:
                ball_text_rect.top -= 1
                ball_rect.top -= 1
                if ball_text_rect.top == height - 10 - ball_text_rect.height:
                    ball_begin_flag = False
            screen.blit(ball_img, (10, ball_rect.top))
            screen.blit(ball_text, (20 + ball_rect.width, ball_text_rect.top))

            # 绘制增加的分数
            if plus > 0:
                plus_temp = plus
                plus_color = ORANGE
                plus_str = '+%d'
                plus_text = score_font.render(plus_str % plus_temp, True, plus_color)
            elif plus < 0:
                plus_temp = plus
                plus_color = RED
                plus_str = '%d'
                plus_text = score_font.render(plus_str % plus_temp, True, plus_color)
            else:
                plus_text = score_font.render(plus_str % plus_temp, True, plus_color)
            plus = 0
            score_text = score_font.render('Score : %d' % score, True, WHITE)
            if score_rect.top < 5:
                score_rect.top += 1
            screen.blit(score_text, score_rect)
            new_score_rect = score_text.get_rect()
            screen.blit(plus_text, (new_score_rect.right + 30, score_rect.top))

            # 启动mian函数时按钮的移动
            if pause.rect.top < 10:
                pause.rect.top += 1
                sound.rect.top += 1
                back.rect.top += 1
            # 绘制按钮
            screen.blit(pause.image, pause.rect)
            screen.blit(back.image, back.rect)
            screen.blit(sound.image, sound.rect)

            # 监测所有敌人是否与主角相撞
            enemy_down = pygame.sprite.spritecollide(myhero, all_enemies, False, pygame.sprite.collide_mask)
            if enemy_down:
                for e in enemy_down:
                    if e != myenemy and e.active:
                        if not myhero.invincible:
                            myhero.hurt_sound.play()
                            myhero.active = False
                            life_num -= 1
                            myhero.invincible = True
                            pygame.time.set_timer(REBORN_TIMER, 3000)
                    elif e == myenemy and e.active:
                        reward.play()
                    e.active = False

            # 绘制剩余生命数量
            if life_num:
                if life_rect.top > 530:
                    for i in range(life_num):
                        life_rect.top -= 1
                        screen.blit(life_image, (width - (i + 1) * (life_rect.width + 10), life_rect.top))
                else:
                    for i in range(life_num):
                        screen.blit(life_image, (width - (i + 1) * (life_rect.width + 10), life_rect.top))
            else:
                # 关闭所有声音
                reward.set_volume(0)
                become_inv.set_volume(0)
                get_supply_sound.set_volume(0)
                supply_sound.set_volume(0)
                car.des_sound.set_volume(0)
                for e in enemies:
                    e.des_sound.set_volume(0)
                rolling.des_sound.set_volume(0)
                wolf.des_sound.set_volume(0)
                stone.des_sound.set_volume(0)
                box.des_sound.set_volume(0)
                tong.des_sound.set_volume(0)
                begin_sound.set_volume(0)
                myhero.music.set_volume(0)
                running_sound.set_volume(0)
                myhero.music.set_volume(0)
                upgrade_sound.set_volume(0)
                pygame.mixer.music.pause()

                if not sound.flag:
                    gameover_sound.set_volume(0.6)
                else:
                    gameover_sound.set_volume(0)
                gameover_sound.play()

                if not recorded:
                    # 写入新的最高分
                    recorded = True
                    if score > record_score:
                        record_score = score
                        dump_score_file = open('record.pkl', 'wb')
                        pickle.dump(record_score, dump_score_file)
                        dump_score_file.close()

                # 获取截屏
                screen_shot = screen.subsurface((0, 0, width, height)).copy()
                # 启动gameover函数
                gameover(score, screen_shot)

            # delay减1
            delay -= 1
            # 若没放走贪官，则补给计数则持续加1
            if (not letgo_flag) and (not level_tip):
                supply_count += 1
            # delay减至0时再重置为100，此时分数加100
            if not delay:
                delay = 100
                score += 100
                # 当出现动态障碍物时，游戏速度变快
                if dynamic_flag and FPS < 130:
                    FPS += 1
        # 暂停后的只需更新暂停按钮和音乐按钮的状态
        else:
            screen.blit(pause.image, pause.rect)
            screen.blit(sound.image, sound.rect)

        # 更新屏幕
        pygame.display.flip()
        # 时间间隔
        clock.tick(FPS)

# 游戏结束的函数
def gameover(score, screen_shot):
    # 游戏结束后的分数文字字体
    gameover_font = pygame.font.Font('src/font/BAUHS93.TTF', 48)
    # 游戏结束的分数值
    final_score = 'Score: %d' % score
    # 游戏结束后的分数文字
    gameover_text = gameover_font.render(final_score, True, WHITE)
    # 游戏结束后的分数文字对应的矩形
    gameover_text_rect = gameover_text.get_rect()

    # 主循环运行的标志
    running = True
    # 更新画面的时间间隔
    clock = pygame.time.Clock()

    # 主循环
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # 点击屏幕则出现关闭动画
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    screen_shot = screen.subsurface((0, 0, width, height)).copy()
                    door_close(screen_shot)

        # 绘制游戏结束的提示框和分数
        if gameover_rect.top < 150:
            gameover_rect.top += 10
        screen.blit(screen_shot, (0,0))
        screen.blit(gameover_img, gameover_rect)
        screen.blit(gameover_text,(470, gameover_rect.bottom - gameover_text_rect.height - 80))

        # 更新画面
        pygame.display.flip()
        # 更新画面的时间间隔
        clock.tick(90)

# 关闭动画的函数
def door_close(screen_shot):
    running = True
    # 计数
    count = 0
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 绘制背景
        screen.blit(screen_shot, (0, 0))
        if up_rect.top < 0:
            up_rect.top += 10
            down_rect.top -= 10
        # 绘制关闭动画的上下两个控件
        screen.blit(gameover_up, up_rect)
        screen.blit(gameover_down, down_rect)

        # 计数开始
        if up_rect.top == 0:
            count += 1
        # 当计数大于等于120，则关闭动画结束，调用打开动画
        if count >= 120:
            door_open()

        # 更新屏幕
        pygame.display.flip()
        # 时间间隔
        clock.tick(90)

# 打开动画的函数
def door_open():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 背景移动
        background1_rect.left -= 4
        background2_rect.left -= 4
        if background1_rect.left <= -1100:
            background1_rect.left = 0
            background2_rect.left = bg_size[0] - 1

        # 绘制背景
        screen.blit(background1, background1_rect)
        screen.blit(background2, background2_rect)

        # 判断打开的控件的位置是否在屏幕内
        if up_rect.bottom > 0:
            up_rect.top -= 10
            down_rect.top += 10
        else:
            # 重置控件的位置和状态
            reset_global()
            begin()

        # 绘制打开动画
        screen.blit(gameover_up, up_rect)
        screen.blit(gameover_down, down_rect)

        pygame.display.flip()
        clock.tick(90)


def begin():
    global record_score
    global start,start_rect,start_unpressed,start_pressed,instruction,instruction_rect,instruction_pressed,instruction_pressed,\
        score_reset,reset_rect,reset_pressed,reset_unpressed,game_exit,exit_rect,exit_unpressed,exit_pressed,record_score,sound

    # 人物小动画
    begin_hero = hero.Hero(bg_size)
    begin_hero.rect.left, begin_hero.rect.bottom = 488, 672

    # 播放背景音乐
    if not sound.flag:
        begin_sound.set_volume(0.8)
    else:
        begin_sound.set_volume(0)
    begin_sound.play(-1)

    # 分数
    best_font = pygame.font.Font('src/font/font.TTF', 24)
    best_text = best_font.render('Best: %d' % record_score, True, WHITE)
    best_text_rect = best_text.get_rect()
    best_text_rect.left, best_text_rect.bottom = 10, 660

    delay = 100
    hero_index = 0
    title_index = 0
    begin_main_flag = False
    running = True
    mouse_enter = False
    # 显示游戏介绍的标志
    instruction_show = False
    instruction_exit = False
    instruction_move = False
    instruction_flag = False
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEMOTION:
                if not instruction_flag:
                    if start_rect.collidepoint(event.pos):
                        start = start_pressed
                        if not mouse_enter:
                            if not sound.flag:
                                button_sound.play()
                            mouse_enter = True

                    elif instruction_rect.collidepoint(event.pos):
                        instruction = instruction_pressed
                        if not mouse_enter:
                            if not sound.flag:
                                button_sound.play()
                            mouse_enter = True

                    elif reset_rect.collidepoint(event.pos):
                        score_reset = reset_pressed
                        if not mouse_enter:
                            if not sound.flag:
                                button_sound.play()
                            mouse_enter = True

                    elif exit_rect.collidepoint(event.pos):
                        game_exit = exit_pressed
                        if not mouse_enter:
                            if not sound.flag:
                                button_sound.play()
                            mouse_enter = True
                    else:
                        mouse_enter = False
                        button_sound.stop()
                        start = start_unpressed
                        instruction = instruction_unpressed
                        score_reset = reset_unpressed
                        game_exit = exit_unpressed

            if event.type == MOUSEBUTTONUP:
                if not instruction_flag:
                    # 点击音乐按钮
                    if event.button == 1 and sound.rect.collidepoint(event.pos):
                        if not sound.flag:
                            begin_sound.set_volume(0)
                            sound.image = sound_off
                        else:
                            sound.image = sound_on
                            begin_sound.set_volume(0.6)
                        sound.flag = not sound.flag
                    # 点击开始游戏开始
                    elif event.button == 1 and start_rect.collidepoint(event.pos):
                        begin_sound.stop()
                        if not sound.flag:
                            running_sound.set_volume(1.0)
                        else:
                            running_sound.set_volume(0)
                        running_sound.play(-1)
                        begin_main_flag = True

                        # 播放背景音乐
                        pygame.mixer.music.play(-1)
                        if sound.flag:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

                    # 点击重置按钮将重置记录
                    elif event.button == 1 and reset_rect.collidepoint(event.pos):
                        pickle_file = open('record.pkl', 'wb')
                        best_score = 0
                        record_score = best_score
                        best_text = best_font.render('Best: %d' % best_score, True, WHITE)
                        pickle.dump(best_score, pickle_file)
                        pickle_file.close()

                    # 点击介绍按钮显示介绍内容
                    elif event.button == 1 and instruction_rect.collidepoint(event.pos):
                        instruction_exit = False
                        instruction_flag = True
                        instruction_show = True
                        instruction_move = True

                    # 点击退出按钮程序退出
                    elif event.button == 1 and exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                # 介绍内容离开画面
                else:
                    instruction_show = False
                    instruction_exit = True
                    instruction_move = True

        # 判断是否从游戏结束后返回开始界面
        if not begin_main_flag:
            if instruction_rect.right < 538:
                start_rect.left += 8
                instruction_rect.left += 8
                reset_rect.left -= 8
                exit_rect.left -= 8
                begin_hero.rect.top -= 4
                best_text_rect.top -= 1
                title.rect.top += 4
            if sound.rect.top < 10:
                sound.rect.top += 1

        # 背景移动
        if not (delay % 2):
            background1_rect.left -= 4
            background2_rect.left -= 4
            if background1_rect.right == 0:
                background1_rect.left = 0
                background2_rect.left = bg_size[0] - 1

        # 标题动画
        if not (delay % 12):
            title_index = (title_index + 1) % 8
            title.image = title.images[title_index]

        # 角色动画
        if not (delay % 8):
            hero_index = (hero_index + 1) % 10
            begin_hero.image = begin_hero.images[hero_index]

        # 判断是否点击了游戏开始的按钮
        if begin_main_flag:
            start = start_unpressed
            if begin_hero.rect.left != 126:
                start_rect.left -= 8
                instruction_rect.left -= 8
                reset_rect.left += 8
                exit_rect.left += 8
                begin_hero.rect.left += 2
                best_text_rect.top += 1
                title.rect.top -= 1
                sound.rect.top -= 1
                if sound.rect.bottom < 0:
                    sound.reset()
                if begin_hero.rect.left >= 1100:
                    begin_hero.rect.right = -1
            else:
                main()

        # 绘制控件
        screen.blit(background1, background1_rect)
        screen.blit(background2, background2_rect)
        screen.blit(title.image, title.rect)
        screen.blit(sound.image, sound.rect)
        screen.blit(start, start_rect)
        screen.blit(instruction, instruction_rect)
        screen.blit(score_reset, reset_rect)
        screen.blit(game_exit, exit_rect)
        screen.blit(begin_hero.image, begin_hero.rect)

        # 绘制最高分
        screen.blit(best_text, best_text_rect)

        # 绘制操作说明
        if instruction_show:
            instruction = instruction_unpressed
            if instruction_move:
                instr_rect.top += 10
            screen.blit(instr, instr_rect)
            if instr_rect.top == (height - instr_rect.height) // 2:
                instruction_move = False
        # 介绍内容退出
        if instruction_exit:
            if instruction_move:
                instr_rect.top += 10
            screen.blit(instr, instr_rect)
            if instr_rect.top == height:
                instruction_move = False
                instruction_flag = False
                instr_rect.left, instr_rect.bottom = 250, 0

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(200)


# 游戏运行
if __name__ == '__main__':
    try:
        # 启动开始时界面
        begin()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()