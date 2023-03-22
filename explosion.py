import pygame
import math


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pygame.Surface((10, 10)),
            pygame.Surface((15, 15)),
            pygame.Surface((25, 25))
        ]
        self.images[0].fill((255, 0, 0))
        self.images[1].fill((255, 165, 0))
        self.images[2].fill((255, 255, 0))
        self.image_index = 0
        self.image = self.images[self.image_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer % 3 == 0:
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.image_index]
