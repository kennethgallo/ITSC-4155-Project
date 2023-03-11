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
        self.speed = 5

    def movement(self, player):
        # Create a direct vector from enemy to player coordinates
        vector = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        if vector.length() > 0:
            vector.normalize()
            # Move along this vector towards the player at current speed
            vector.scale_to_length(self.speed)
            self.rect.move_ip(vector)

    def change_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.kill()
            return True
        else:
            return False

    def update(self, player):
        self.movement(player)
