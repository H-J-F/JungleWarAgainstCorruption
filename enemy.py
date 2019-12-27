import pygame
from random import randint

#敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, bg_size, image_list, des_imgs, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = pygame.image.load('src/image/widgets/names/%s.png' % name).convert_alpha()
        self.name_rect = self.name.get_rect()
        if name != "GXQ":
            self.des_sound = pygame.mixer.Sound('src/sounds/mancry.wav')
            self.name_rect.top = 220
        else:
            self.des_sound = pygame.mixer.Sound('src/sounds/girlcry.wav')
            self.name_rect.top = 180
        self.des_sound.set_volume(0.6)
        self.destroy_imgs = des_imgs
        self.images = []
        for img in image_list:
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.active = True
        self.mask = pygame.mask.from_surface(self.images[0])
        self.rect.left, self.rect.bottom = randint(1100, 1500), 400

    def setMask(self, index):
        self.mask = pygame.mask.from_surface(self.images[index])

    def reset(self):
        self.speed = 2
        self.active = True
        self.rect.left, self.rect.bottom = randint(1100, 1500), 400

    def move(self):
        self.rect.left -= self.speed