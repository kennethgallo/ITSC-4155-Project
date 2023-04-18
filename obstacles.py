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

        # if x_pos < 0:  # if obstacles.x_pos < 0:
        #    y_pos = random.randint(0, 500)

        # if y_pos < 0:  # if obstacles.y_pos < 0:
        #    x_pos = random.randint(0, 500)

    def draw_obstacle(self, display_surface):  # (display_surface):
        # follow draw_healthbar in player.py and enemy.py
        # maybe also follow
        # https://www.techwithtim.net/tutorials/game-development-with-python/side-scroller-pygame/random-object-generation/
        display_surface.blit('Assets/fence_00.png', display_surface)
        # can I use self.rect instead of making a hitbox? (the hitbox is following the techwithtim tutorial)
        # self.hitbox = (self.x + 10, self.y + 10)
        self.rect = self.image.get_rect()

        # main 226 - Check if the projectile collides with the enemy
        # if pygame.sprite.collide_rect(projectile, enemy):

        # main 258 - Check if an enemy sprite has collided with a player sprite
        # if pygame.sprite.spritecollideany(enemy, player_sprite):

    # Logic for player collision with obstacles ???
    # def check_collision(self, player):
    #    for obstacles in obstacles_sprites:
    #        if pygame.sprite.spritecollideany(player, obstacles):
    #           some code

    # Logic for enemy collision with obstacles ???
    # def check_collision(self, enemy):
    #    for obstacles in obstacles_sprites:
    #        if pygame.sprite.spritecollideany(enemy, obstacles):
    #           some code

    # Do I need to do a function in player and enemy similar to
    # def check_collision(self, enemies): and def move_back_from_player(self): from enemy

# Tasks:
# 1. How to draw to surface with size restrictions - DONE: "all_sprites.draw(display_surface)" in Main

# 2. How to draw to surface with collisions
# Recreate line 217 in main.py (if pygame.sprite.spritecollideany)
# for player and enemy colliding with obstacle
# I might have to do the logic for enemy collisions with obstacles in the
# enemy.py class and the player collisions in player.py
# enemy.py has def check_collision(self, enemies):

# 3. How to randomly draw to surface with size restrictions - look at the directions in enemy_spawn
# ( line 38 - def spawn_enemies(self, curr_round): )

# 4. Do logic in main for drawing an obstacle at a random position at the start of the game
# (ie look in main.py for beginning of loop for game) -

# 5. Do logic in main for creating the obstacle(s) (line 127) - DONE

# 6. Do logic in main for adding the obstacle(s) to the map (line x) - DONE

# Fence in Assets folder of project in GitHub
