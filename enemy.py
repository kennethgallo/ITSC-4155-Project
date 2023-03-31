import pygame
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, index, start_health, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load('Assets/enemy/enemy1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.health = start_health
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.max_speed = 5
        self.speed = self.max_speed
        self.vector = pygame.math.Vector2(0, 0)
        self.last_collision_time = pygame.time.get_ticks()

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

    def check_collision(self, enemies):
        for enemy2 in enemies:
            if self.rect.colliderect(enemy2) and self != enemy2:

                x_dist = self.rect.x - enemy2.rect.x
                y_dist = (self.rect.y - enemy2.rect.y) * -1
                distance_radius = math.sqrt((x_dist ** 2) + (y_dist ** 2))
                distance_limit = 20

                if distance_radius < distance_limit:
                    distance_needed = distance_limit - distance_radius
                    if x_dist == 0:
                        if y_dist > 0:
                            angle_needed = 90
                        else:
                            angle_needed = -90
                    else:
                        angle_needed = math.degrees(math.atan(y_dist / x_dist))
                        if x_dist < 0 and y_dist < 0:
                            angle_needed += 180

                    cos_x = math.cos(math.radians(angle_needed))
                    sin_y = math.sin(math.radians(angle_needed))
                    x_dist_needed = cos_x * distance_needed
                    y_dist_needed = sin_y * distance_needed

                    self.rect.y += y_dist_needed * -1
                    self.rect.x += x_dist_needed

    def update(self, player, enemies):
        self.movement(player)
        self.check_collision(enemies)
