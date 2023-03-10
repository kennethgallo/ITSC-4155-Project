import pygame
from enemy_spawn import enemy_spawn_points


class Enemy(pygame.sprite.Sprite):
    def __init__(self, index, start_health):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.health = start_health
        self.enemy_x = enemy_spawn_points[index][0]
        self.enemy_y = enemy_spawn_points[index][1]

    def movement(self):
        self.rect.x = self.enemy_x
        self.rect.y = self.enemy_y

    def change_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.kill()

    def update(self):
        self.movement()
