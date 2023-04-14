import pygame
import math
from projectile import Projectile


class Enemy(pygame.sprite.Sprite):
    def __init__(self, index, start_health, x_pos, y_pos, all_sprites, enemy_projectiles, enemy_type):
        super().__init__()
        if enemy_type == 'melee':
            self.image = pygame.image.load('Assets/enemy/enemy1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
        elif enemy_type == 'projectile':
            self.image = pygame.image.load('Assets/enemy/enemy1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.max_projectile_cooldown = 50
            self.projectile_cooldown = self.max_projectile_cooldown
        elif enemy_type == 'exploding':
            self.image = pygame.image.load('Assets/enemy/enemy1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect()

        self.all_sprites = all_sprites
        self.enemy_projectiles = enemy_projectiles

        self.start_health = start_health
        self.health = start_health

        self.enemy_type = enemy_type  # melee or projectile

        self.rect.x = x_pos
        self.rect.y = y_pos

        if enemy_type == 'exploding':
            self.max_speed = 7.5
        else:
            self.max_speed = 5
        self.speed = self.max_speed
        self.vector = pygame.math.Vector2(0, 0)
        self.last_collision_time = pygame.time.get_ticks()

    def movement(self, player):

        # Create a direct vector from enemy to player coordinates
        self.vector = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)

        if self.enemy_type == 'melee' or self.enemy_type == 'exploding':

            # If moving away from the player, start moving back slowly
            if self.speed < self.max_speed:
                self.speed += 0.25
                if self.speed > self.max_speed:
                    self.speed = self.max_speed

            # Move along this vector towards the player at current speed
            if self.vector.length() > 0:
                self.vector.normalize()
                self.vector.scale_to_length(self.speed)
                self.rect.move_ip(self.vector)

        elif self.enemy_type == 'projectile':

            # Shoot at the player
            if self.vector.length() > 0 and self.projectile_cooldown <= 0:
                self.vector.normalize()
                dx = self.vector.x
                dy = self.vector.y
                direction = math.degrees(math.atan2(-dy, dx))
                projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
                self.all_sprites.add(projectile)
                self.enemy_projectiles.add(projectile)
                self.projectile_cooldown = self.max_projectile_cooldown

    def move_back_from_player(self):
        self.speed = -5

    def change_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.kill()
            return True
        else:
            return False

    def draw_healthbar(self, display_surface):
        red = (255, 0, 0)
        green = (0, 255, 0)

        barx = self.rect.x
        bary = self.rect.y

        background_length = 110
        foreground_length = (float(self.health) / float(self.start_health)) * background_length

        pygame.draw.rect(display_surface, red, (barx - 25, bary - 25, background_length, 10))
        pygame.draw.rect(display_surface, green, (barx - 25, bary - 25, foreground_length, 10))

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

        if self.enemy_type == 'projectile':
            self.projectile_cooldown -= 1
