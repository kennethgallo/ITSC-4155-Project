import pygame
import math


# remember to push changes of main.py to github
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.image.load('Assets/fence_00.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.obstacle_y = 400
        self.obstacle_x = 400

# Want to have a random obstacle(s) generated in random positions.
# The obstacle(s) can't be huge (ie not as long or wide as the bounds of the map).
# The obstacle(s) should be (at most) a certain percent of the bounds of the map
    # (ie <= 10% of the length and width of map bounds).

# Tasks:
# 1. How to draw to surface with size restrictions
# 2. How to randomly draw to surface with size restrictions
# 3. Do logic in main for drawing an obstacle at a random position at the start of the game
    # (ie look in main.py for beginning of loop for game)
# 4. Do logic in main for creating the obstacle(s) (line 127),
# 5. Do logic in main for adding the obstacle(s) to the map (line x)
# 6. Recreate line 177 in main.py (if pygame.sprite.spritecollideany)
    # for player and enemy colliding with obstacle

# Fence in Assets folder of project in Github


