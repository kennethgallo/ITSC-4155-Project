import pygame
import random


class ItemDrop(pygame.sprite.Sprite):
    def __init__(self, item_type, location):
        super().__init__()

        self.item_type = item_type

        self.image = pygame.surface.Surface((30, 30))
        if item_type == 'health':
            self.image.fill('Green')
        else:
            self.image.fill('Yellow')
        self.rect = self.image.get_rect()
        self.rect.center = location


def roll_drop():
    random_number = random.randint(0, 100)
    if random_number < 60:
        return None
    elif random_number < 80:
        return 'health'
    else:
        return 'money'
