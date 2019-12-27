import pygame

# 天使类
class Angel(pygame.sprite.Sprite):
    def __init__(self, bg_size, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.begin = True
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.bottom = 790, 0

    def reset(self):
        self.begin = True
        self.rect.left, self.rect.bottom = 790, 0

    def move(self):
        if self.begin:
            if self.rect.bottom < 122:
                self.rect.bottom += 3
            else:
                self.begin = False
        else:
            self.rect.bottom += self.speed
            if self.rect.bottom  == 147:
                self.speed = -self.speed
            elif self.rect.bottom == 117:
                self.speed = -self.speed

# 补给类
class Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 0.2
        self.speedx = 6
        self.speedy = 1
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = 770, 100

    def reset(self):
        self.active = False
        self.speedx = 6
        self.speedy = 1
        self.rect.left, self.rect.top = 770, 100

    def move(self):
        self.rect.left -= self.speedx
        if self.rect.bottom < 400:
            self.speedy += self.speed
            self.rect.bottom += self.speedy
            if self.rect.bottom > 400:
                self.rect.bottom = 400
                self.speedx = 4
        else:
            self.rect.bottom = 400