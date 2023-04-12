import pygame
import math


class Projectile(pygame.sprite.Sprite):

    max_hits = 1

    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction
        self.hit_count = 0
        self.hit_enemies = set()

    def update(self):
        # Calculate direction vector
        dx = math.cos(math.radians(self.direction)) * self.speed
        dy = -math.sin(math.radians(self.direction)) * self.speed

        # Update position
        self.rect.x += dx
        self.rect.y += dy

    def has_hit(self, enemy):
        return enemy in self.hit_enemies

    def mark_hit(self, enemy):
        self.hit_enemies.add(enemy)
