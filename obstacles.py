import pygame
import random
# remember to push changes of main.py to github


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, surf, groups):  # (self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.image.load('Assets/fence_00.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        if x_pos < 0:          # if obstacles.x_pos < 0:
            y_pos = random.randint(0, 500)

        if y_pos < 0:         # if obstacles.y_pos < 0:
            x_pos = random.randint(0, 500)

# Want to have a random obstacle(s) generated in random positions.
# The obstacle(s) can't be huge (ie not as long or wide as the bounds of the map).
# The obstacle(s) should be (at most) a certain percent of the bounds of the map
    # (ie <= 10% of the length and width of map bounds).

# Tasks:
# 1. How to draw to surface with size restrictions - DONE: "all_sprites.draw(display_surface)" in Main

# 2. How to randomly draw to surface with size restrictions - DONE? (logic of randint in obstacles.py)

# 3. Do logic in main for drawing an obstacle at a random position at the start of the game
    # (ie look in main.py for beginning of loop for game) - DONE? (logic of randint in obstacles.py)

# 4. Do logic in main for creating the obstacle(s) (line 127) - DONE

# 5. Do logic in main for adding the obstacle(s) to the map (line x) - DONE

# 6. Recreate line 217 in main.py (if pygame.sprite.spritecollideany)
    # for player and enemy colliding with obstacle
    # I might have to do the logic for enemy collisions with obstacles in the enemy.py class

# 7. Use same logic for how the player sprite was added to the player obj
    # for how to add the fence sprite to the fence obj

# Fence in Assets folder of project in Github

