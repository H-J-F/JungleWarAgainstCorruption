import pygame
from random import randint

# 动态障碍类
class DynamicBlock(pygame.sprite.Sprite):
    def __init__(self, bg_size, image_list, speed, index, bottom, des_imgs):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for img in image_list:
            self.images.append(img)
        self.destroy_imgs = des_imgs
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.temp_speed = speed
        self.speed = self.temp_speed
        self.bottom = bottom
        self.block_index = 0
        self.index = index
        self.distance = 3000
        self.active = True
        self.away = True
        self.mask = pygame.mask.from_surface(self.images[0])
        self.rect.left, self.rect.bottom = randint(1100, self.distance), self.bottom

    def setMask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        self.speed = self.temp_speed
        self.active = True
        self.away = True
        self.rect.left, self.rect.bottom = randint(1100, self.distance), self.bottom

    def move(self):
        self.rect.left -= self.speed

# 静态障碍类
class StaticBlock(pygame.sprite.Sprite):
    def __init__(self, bg_size, image, des_imgs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.destroy_imgs = des_imgs
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 4
        self.distance = 2000
        self.active = True
        self.away = True
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.bottom = randint(1100, self.distance), 400

    def reset(self):
        self.active = True
        self.away = True
        self.rect.left, self.rect.bottom = randint(1100, self.distance), 400

    def move(self):
        self.rect.left -= self.speed

# 炮弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bg_size, image, des_imgs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.des_sound = pygame.mixer.Sound('src/sounds/me_down.wav')
        self.destroy_imgs = des_imgs
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 13
        self.distance = 7000
        self.active = True
        self.away = True
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.bottom = randint(1100, self.distance), randint(50, 400)

    def reset(self):
        self.active = True
        self.away = True
        self.rect.left, self.rect.bottom = randint(1100, self.distance), randint(50, 400)

    def move(self):
        self.rect.left -= self.speed