import pygame
from projectile import Projectile
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height, health, all_sprites, projectiles):
        super().__init__()
        self.image = pygame.image.load('Assets/playerRight.png').convert_alpha()
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

    def change_asset(self, direction):
        self.image = pygame.image.load('Assets/player' + direction + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))

    def key_movement(self):
        # Find keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 0:
            self.change_asset("back")
            self.player_y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < self.window_height:
            self.change_asset("front")
            self.player_y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.change_asset("left")
            self.player_x -= self.speed
        if keys[pygame.K_d] and self.rect.right < self.window_width:
            self.change_asset("right")
            self.player_x += self.speed
        if pygame.mouse.get_pressed()[0] and self.projectile_cooldown <= 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
            direction = math.degrees(math.atan2(-dy, dx))

            projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
            self.all_sprites.add(projectile)
            self.projectiles.add(projectile)
            self.projectile_cooldown = 15

        # Update rect values to move player
        self.rect.x += self.player_x
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
