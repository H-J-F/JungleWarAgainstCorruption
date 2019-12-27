import pygame

# 控件类
class Widget(pygame.sprite.Sprite):
    def __init__(self, bg_size, image_list, pos):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        for img in image_list:
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x, self.y = pos
        self.rect.left, self.rect.bottom = self.x, self.y

    def reset(self):
        self.rect.left, self.rect.bottom = self.x, self.y

# 按钮类
class Button(pygame.sprite.Sprite):
    def __init__(self, bg_size, image, pos):
        pygame.sprite.Sprite.__init__(self)

        self.default_image = image
        self.image = self.default_image
        self.flag = False
        self.rect = self.image.get_rect()
        self.x, self.y = pos
        self.rect.left, self.rect.bottom = self.x, self.y

    def reset(self):
        self.rect.left, self.rect.bottom = self.x, self.y