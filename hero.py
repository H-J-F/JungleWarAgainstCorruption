import pygame

# 主角类
class Hero(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.inv_imgs = []
        self.mask_imgs = []
        self.music = pygame.mixer.Sound('src/sounds/he.wav')
        self.music.set_volume(0.8)
        self.hurt_sound = pygame.mixer.Sound('src/sounds/hurt.wav')
        self.hurt_sound.set_volume(0.8)
        self.images.extend([pygame.image.load('src/image/hero/1.png').convert_alpha(),
                            pygame.image.load('src/image/hero/2.png').convert_alpha(),
                            pygame.image.load('src/image/hero/3.png').convert_alpha(),
                            pygame.image.load('src/image/hero/4.png').convert_alpha(),
                            pygame.image.load('src/image/hero/5.png').convert_alpha(),
                            pygame.image.load('src/image/hero/6.png').convert_alpha(),
                            pygame.image.load('src/image/hero/7.png').convert_alpha(),
                            pygame.image.load('src/image/hero/8.png').convert_alpha(),
                            pygame.image.load('src/image/hero/9.png').convert_alpha(),
                            pygame.image.load('src/image/hero/10.png').convert_alpha(),
                            pygame.image.load('src/image/hero/11.png').convert_alpha(),
                            pygame.image.load('src/image/hero/12.png').convert_alpha()])
        self.inv_imgs.extend([pygame.image.load('src/image/supply/invincible/1.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/2.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/3.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/4.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/5.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/6.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/7.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/8.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/9.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/10.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/11.png').convert_alpha(),
                              pygame.image.load('src/image/supply/invincible/12.png').convert_alpha()])
        self.mask_imgs.extend([pygame.image.load('src/image/hero/mask/1.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/2.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/3.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/4.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/5.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/6.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/7.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/8.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/9.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/10.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/11.png').convert_alpha(),
                               pygame.image.load('src/image/hero/mask/12.png').convert_alpha()])
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        self.temp_imgs = self.images
        self.switch_img = False
        self.invincible = False
        self.music_flag = True
        self.active = True
        self.uninvincible = False
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 20
        self.mask = pygame.mask.from_surface(self.images[0])
        self.rect.left, self.rect.top = 130, self.height - self.rect.height - 200

    def jump(self):
        if self.music_flag:
            self.music.play()
            self.music_flag = False
        self.rect.top -= self.speed
        self.speed -= 1.5

    def resetSpeed(self):
        self.speed = 20

    def reset(self):
        self.uninvincible = False
        self.switch_img = False
        self.active = True
        self.invincible = False

    def resetPos(self):
        self.rect.bottom = 400

    def setMask(self, index):
        self.mask = pygame.mask.from_surface(self.mask_imgs[index])