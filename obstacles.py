import pygame
import random


# remember to push changes of main.py to github


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos): # (self, x_pos, y_pos, surf):  (x value, y value, width, height)
        super().__init__()
        self.image = pygame.image.load('Assets/fence_00.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  # changed from (50, 50)
        # self.rect.x = x_pos
        # self.rect.y = y_pos
        self.rect = self.image.get_rect()
        self.rect.center = (200, 300)

    def draw_obstacle(self, display_surface):  # (display_surface):
        display_surface.blit('Assets/fence_00.png', display_surface)
        self.rect = self.image.get_rect()

    # Logic to block overlapping movement with the obstacles (from gamedev stackexchange)
    # Will this need to go in player.py and enemy.py. BOTH
    # for obstacle in obstacles:
    #    if player.mask.overlap(obstacle.mask, offset):
    #        blocked_dir = player.direction
    #    else:
    #        blocked_dir = ''

    # movement - (from player.py in my case)
    # - Will this need to go in player.py and enemy.py . YES
#    if key_pressed[K_d] and blocked_dir != 'right':
#        player.x += player.speed
#    elif key_pressed[K_w] and blocked_dir != 'up':
#        player.y -= player.speed
#    elif key_pressed[K_a] and blocked_dir != 'left':
#        player.x -= player.speed
#    elif key_pressed[K_s] and blocked_dir != 'down':
#        player.y += player.speed


# Fence in Assets folder of project in GitHub
