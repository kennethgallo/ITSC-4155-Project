import pygame
from projectile import Projectile
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height, health, all_sprites, projectiles):
        super().__init__()
        self.image = pygame.image.load('Assets/player/newPlayerRight1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.health = health
        self.player_y = 500
        self.player_x = 500
        self.speed = 10
        self.window_width = window_width
        self.window_height = window_height
        self.all_sprites = all_sprites
        self.projectiles = projectiles
        self.projectile_cooldown = 0
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0

        # Loads all the animation frames into a list
        self.left_anim = [pygame.image.load('Assets/player/newPlayerLeft1.png').convert_alpha(),
                          pygame.image.load('Assets/player/newPlayerLeft2.png').convert_alpha(),
                          pygame.image.load('Assets/player/newPlayerLeft3.png').convert_alpha()]

        self.right_anim = [pygame.image.load('Assets/player/newPlayerRight1.png').convert_alpha(),
                           pygame.image.load('Assets/player/newPlayerRight2.png').convert_alpha(),
                           pygame.image.load('Assets/player/newPlayerRight3.png').convert_alpha()]

    def swap_asset(self, direction, number):
        #  Chooses the right list, will be refactored for up and down animation
        anim_list = self.left_anim if direction == "Left" else self.right_anim

        #  Uses the number variable to determine correct frame then displays it
        frame_index = (number - 1) % len(anim_list)
        self.image = anim_list[frame_index]

        #  The player kept changing sizes so this keeps him constant
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.player_x -= self.speed

    def key_movement(self):
        # Find keys pressed
        keys = pygame.key.get_pressed()

        # Left player movement
        if keys[pygame.K_a] and self.rect.left > 0:
            self.swap_asset("Left", int(pygame.time.get_ticks() / 500) % 5 + 1)
            self.rect.x -= self.speed

        # Right player movement
        if keys[pygame.K_d] and self.rect.right < self.window_width:
            self.swap_asset("Right", int(pygame.time.get_ticks() / 500) % 5 + 1)
            self.rect.x += self.speed

        # Up player movement
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed

        # Down player movement
        if keys[pygame.K_s] and self.rect.bottom < self.window_height:
            self.rect.y += self.speed

        if pygame.mouse.get_pressed()[0] and self.projectile_cooldown <= 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
            direction = math.degrees(math.atan2(-dy, dx))

            projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
            self.all_sprites.add(projectile)
            self.projectiles.add(projectile)
            self.projectile_cooldown = 15

        self.rect.y += self.player_y

        # Reset movement for next time
        self.player_x = 0
        self.player_y = 0

    def change_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.kill()

    def update(self):
        self.key_movement()
        self.projectile_cooldown -= 1
