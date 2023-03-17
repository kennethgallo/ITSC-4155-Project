import pygame
from enemy_spawn import enemy_spawn_points


class Enemy(pygame.sprite.Sprite):
    def __init__(self, index, start_health):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.health = start_health
        self.rect.x = enemy_spawn_points[index][0]
        self.rect.y = enemy_spawn_points[index][1]
        self.max_speed = 5
        self.speed = self.max_speed
        self.vector = pygame.math.Vector2(0, 0)

    def movement(self, player):
        # If moving away from the player, start moving back slowly
        if self.speed < self.max_speed:
            self.speed += 0.25
            if self.speed > self.max_speed:
                self.speed = self.max_speed

        # Create a direct vector from enemy to player coordinates
        self.vector = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        if self.vector.length() > 0:
            self.vector.normalize()
            # Move along this vector towards the player at current speed
            self.vector.scale_to_length(self.speed)
            self.rect.move_ip(self.vector)

    def move_back_from_player(self):
        self.speed = -5

    def change_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.kill()
            return True
        else:
            return False

    def update(self, player):
        self.movement(player)
