import pygame

# from main import obstacles_sprites, obstacles
from projectile import Projectile
import math
from upgrade_menu import UpgradeMenu
from sounds import player_death_sound, projectile_sound


class Player(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height, start_health, all_sprites, projectiles):
        super().__init__()
        self.image = pygame.image.load('Assets/player/newPlayerRight1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        self.start_health = start_health
        self.health = start_health
        self.max_invincibility_cooldown = 30
        self.invincibility_cooldown = 0
        self.invincibility_color_fill = (0, 0, 0)

        self.player_y = 500
        self.player_x = 500

        self.speed = 5
        self.money = 0
        self.damage = 15
        self.window_width = window_width
        self.window_height = window_height

        self.all_sprites = all_sprites
        self.projectiles = projectiles
        self.projectile_cooldown = 0
        self.shotgun_cooldown = 0

        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
        self.upgrade_menu = UpgradeMenu(self, projectiles, window_width, window_height)

        self.numKilled = 0

        # Loads all the animation frames into a list
        self.left_anim = [pygame.image.load('Assets/player/newPlayerLeft1.png').convert_alpha(),
                          pygame.image.load('Assets/player/newPlayerLeft2.png').convert_alpha(),
                          pygame.image.load('Assets/player/newPlayerLeft3.png').convert_alpha()]

        self.right_anim = [pygame.image.load('Assets/player/newPlayerRight1.png').convert_alpha(),
                           pygame.image.load('Assets/player/newPlayerRight2.png').convert_alpha(),
                           pygame.image.load('Assets/player/newPlayerRight3.png').convert_alpha()]

        self.up_anim = [pygame.image.load('Assets/player/newPlayerUp1.png').convert_alpha(),
                        pygame.image.load('Assets/player/newPlayerUp2.png').convert_alpha(),
                        pygame.image.load('Assets/player/newPlayerUp3.png').convert_alpha()]

        self.down_anim = [pygame.image.load('Assets/player/newPlayerDown1.png').convert_alpha(),
                          pygame.image.load('Assets/player/newPlayerDown2.png').convert_alpha(),
                          pygame.image.load('Assets/player/newPlayerDown3.png').convert_alpha()]

    def swap_asset(self, direction, number):
        #  Chooses the right list
        if direction == "Left":
            anim_list = self.left_anim
        else:
            if direction == "Right":
                anim_list = self.right_anim
            else:
                if direction == "Down":
                    anim_list = self.up_anim
                else:
                    anim_list = self.down_anim

        #  Uses the number variable to determine correct frame then displays it
        frame_index = (number - 1) % len(anim_list)
        self.image = anim_list[frame_index]

        #  The player kept changing sizes so this keeps him constant
        self.image = pygame.transform.scale(self.image, (60, 60))

    def key_movement(self):
        # Find keys pressed
        keys = pygame.key.get_pressed()

        # Left player movement
        if keys[pygame.K_a] and self.rect.left > 0:
            self.swap_asset("Left", int(pygame.time.get_ticks() / 100) % 5 + 1)
            self.rect.x -= self.speed

        # Right player movement
        if keys[pygame.K_d] and self.rect.right < self.window_width:
            self.swap_asset("Right", int(pygame.time.get_ticks() / 100) % 5 + 1)
            self.rect.x += self.speed

        # Up player movement
        if keys[pygame.K_w] and self.rect.top > 0:
            self.swap_asset("Up", int(pygame.time.get_ticks() / 100) % 5 + 1)
            self.rect.y -= self.speed

        # Down player movement
        if keys[pygame.K_s] and self.rect.bottom < self.window_height:
            self.swap_asset("Down", int(pygame.time.get_ticks() / 100) % 5 + 1)
            self.rect.y += self.speed

        # Check if button B is pressed and display upgrade menu
        if keys[pygame.K_b]:
            self.upgrade_menu.run_menu()

        if pygame.mouse.get_pressed()[0] and self.projectile_cooldown <= 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
            direction = math.degrees(math.atan2(-dy, dx))

            projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
            self.all_sprites.add(projectile)
            self.projectiles.add(projectile)
            self.projectile_cooldown = 30

            # play projectile sound
            projectile_sound()

        if pygame.mouse.get_pressed()[2] and self.shotgun_cooldown <= 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i in range(-30, 45, 15):
                dx = mouse_x - self.rect.centerx
                dy = mouse_y - self.rect.centery
                direction = math.degrees(math.atan2(-dy, dx))
                direction += i

                projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
                self.all_sprites.add(projectile)
                self.projectiles.add(projectile)
                self.shotgun_cooldown = 120

            # play projectile sound
            projectile_sound()

        self.rect.y += self.player_y

        # Reset movement for next time
        self.player_x = 0
        self.player_y = 0

    def change_health(self, amount):

        # check if health is decreasing
        if amount < 0:
            # If cooldown is still counting, don't take damage
            if self.invincibility_cooldown > 0:
                return
            # otherwise, reset the cooldown and brighten the character so the player knows
            else:
                self.invincibility_cooldown = self.max_invincibility_cooldown
                self.invincibility_color_fill = (128, 128, 128)

        self.health += amount
        if self.health > self.start_health:
            self.health = self.start_health

        screen = pygame.display.get_surface()
        if self.health <= 0:
            self.kill()

            # play player death sound
            player_death_sound()

    def draw_healthbar(self, display_surface):
        red = (255, 0, 0)
        green = (0, 255, 0)

        barx = self.rect.x
        bary = self.rect.y

        background_length = 110
        foreground_length = (float(self.health) / float(self.start_health)) * background_length

        pygame.draw.rect(display_surface, red, (barx - 25, bary - 25, background_length, 10))
        pygame.draw.rect(display_surface, green, (barx - 25, bary - 25, foreground_length, 10))

    def update(self):
        self.key_movement()
        self.projectile_cooldown -= 1
        self.shotgun_cooldown -= 1

        # decrease invincibility cooldown
        if self.invincibility_cooldown > 0:
            self.invincibility_cooldown -= 1

            # if cooldown ended, reverse the brightening of the character
            if self.invincibility_cooldown <= 0:
                self.invincibility_color_fill = (0, 0, 0)

        # update the player with a brighter color if invincible, otherwise it will be unaltered
        self.image.fill(self.invincibility_color_fill, special_flags=pygame.BLEND_RGB_ADD)

'''
    # Logic for player collision with obstacles
    def check_collision(self, obstacles):
        for obstacles in obstacles_sprites:
            # if pygame.sprite.spritecollideany(self, obstacles):
            if self.rect.colliderect(obstacles.rect):
                # some code
                print("Player collides with obstacle")
                pass
'''
