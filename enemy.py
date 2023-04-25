import pygame
import math
from projectile import Projectile
from sounds import projectile_sound
# from main import obstacles_sprites, obstacles


class Enemy(pygame.sprite.Sprite):
    def __init__(self, index, start_health, x_pos, y_pos, all_sprites, enemy_projectiles, enemy_type):
        super().__init__()

        if enemy_type == 'melee':
            self.sprite_sheet = pygame.image.load('Assets/enemy/Characters/Spider/Spider-variation1-walk.png').convert_alpha()
            self.start_health = start_health
        elif enemy_type == 'projectile':
            self.sprite_sheet = pygame.image.load('Assets/enemy/Characters/Skeleton/skeleton-variation1-walk.png').convert_alpha()
            self.max_projectile_cooldown = 50
            self.projectile_cooldown = self.max_projectile_cooldown
            self.start_health = start_health
        elif enemy_type == 'exploding':
            self.sprite_sheet = pygame.image.load('Assets/enemy/Characters/Big Worm 1/Big worm - 1-idle-8 frames.png').convert_alpha()
            self.start_health = start_health / 2

        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (60, 60))

        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (480, 60))
        self.frame_width = 60
        self.frame_height = 60
        self.frames = []
        self.last_frame_time = pygame.time.get_ticks()
        for i in range(8):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
            frame_image.blit(self.sprite_sheet, (0, 0), rect)
            self.frames.append(frame_image)
        self.image_index = 0
        self.image = self.frames[self.image_index]

        self.rect = self.image.get_rect()

        self.all_sprites = all_sprites
        self.enemy_projectiles = enemy_projectiles

        self.health = self.start_health
        self.enemy_type = enemy_type  # melee, projectile, or exploding

        self.rect.x = x_pos
        self.rect.y = y_pos

        if enemy_type == 'exploding':
            self.max_speed = 5.5
        else:
            self.max_speed = 3
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
                projectile_sound()

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
        if self.enemy_type in ['melee', 'projectile', 'exploding']:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time > 100:
                self.image_index = (self.image_index + 1) % len(self.frames)
                self.image = self.frames[self.image_index]
                self.last_frame_time = current_time

        self.movement(player)
        self.check_collision(enemies)

        if self.enemy_type == 'projectile':
            self.projectile_cooldown -= 1

    # Logic for enemy collision with obstacles
    '''
    def check_collision(self, obstacle):
         for obstacles in obstacles_sprites:
             if pygame.sprite.spritecollideany(self, obstacles):
                # some code
                print("Player collides with obstacle")
    '''
