import pygame
import random


# remember to push changes of main.py to github


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):  # (self, x_pos, y_pos, surf):
        self.image = pygame.image.load('Assets/fence_00.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        # self.rect.x = x_pos
        # self.rect.y = y_pos
        self.rect = self.image.get_rect()
        self.rect.center = (200, 300)

        if x_pos < 0:  # if obstacles.x_pos < 0:
            y_pos = random.randint(0, 500)

        if y_pos < 0:  # if obstacles.y_pos < 0:
            x_pos = random.randint(0, 500)

    # @staticmethod
    def draw_obstacle(display_surface):
        # follow draw_healthbar in player.py and enemy.py
        # maybe also follow
        # https://www.techwithtim.net/tutorials/game-development-with-python/side-scroller-pygame/random-object-generation/
        display_surface.blit('Assets/fence_00.png', display_surface)

# Tasks:
# 1. How to draw to surface with size restrictions - DONE: "all_sprites.draw(display_surface)" in Main

# 2. How to randomly draw to surface with size restrictions -

# 3. Do logic in main for drawing an obstacle at a random position at the start of the game
# (ie look in main.py for beginning of loop for game) -

# 4. Do logic in main for creating the obstacle(s) (line 127) - DONE

# 5. Do logic in main for adding the obstacle(s) to the map (line x) - DONE

# 6. Recreate line 217 in main.py (if pygame.sprite.spritecollideany)
# for player and enemy colliding with obstacle
# I might have to do the logic for enemy collisions with obstacles in the
# enemy.py class and the player collisions in player.py
# enemy.py has def check_collision(self, enemies):

# 7. Use same logic for how the player sprite was added to the player obj
# for how to add the fence sprite to the fence obj

# Fence in Assets folder of project in GitHub
