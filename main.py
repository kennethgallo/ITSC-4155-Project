import sys
import pygame
from pytmx.util_pygame import load_pygame

import sounds
from player import Player
from button import Button
from text_display import TextDisplay
from enemy_spawn import EnemySpawner
from tile import Tile
from explosion import Explosion
from sounds import main_loop_sounds
from obstacles import Obstacles


# Initialize pygame
pygame.init()

# Create display surface
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()

# Music by Davin St Rose

# pygame.mixer.music.load('Music/gameloop2.mp3')
# pygame.mixer.music.play(-1, 0.0)
# pygame.mixer.music.set_volume(0.15)


# set FPS and clock (allows for controlling movement speed regardless of machine speed)
# FPS can be changed to update movement of the character if needed
FPS = 60
clock = pygame.time.Clock()

# Main menu surface
menu_background_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
menu_background_surface.fill('White')

title_font = pygame.font.Font(None, 28)
title_text = title_font.render('Game Title Main Menu', True, (0, 0, 0), (255, 255, 255))
title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, 100))

# Main menu buttons
menu_buttons = pygame.sprite.Group()
# Start button
start_button = Button('Start', 'White', 'Black', 200, 100)
start_button.rect.center = (WINDOW_WIDTH * (1 / 3), WINDOW_HEIGHT / 2)
# Quit button
quit_button = Button('Quit', 'White', 'Black', 200, 100)
quit_button.rect.center = (WINDOW_WIDTH * (2 / 3), WINDOW_HEIGHT / 2)

menu_buttons.add(start_button)
menu_buttons.add(quit_button)

# Main menu loop
main_menu = True
while main_menu:
    pygame.mixer.music.load('Music/gameloop2.mp3')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.01)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            main_menu = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.rect.collidepoint(mouse_pos):
                main_menu = False
            elif quit_button.rect.collidepoint(mouse_pos):
                main_menu = False
                pygame.quit()
                sys.exit()

    display_surface.blit(menu_background_surface, (0, 0))
    display_surface.blit(title_text, title_rect)
    menu_buttons.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

# Create all_sprites group
all_sprites = pygame.sprite.Group()

# Create explosion_sprites group
explosion_sprites = pygame.sprite.Group()

# Create projectiles group
projectiles = pygame.sprite.Group()

player_sprite = pygame.sprite.GroupSingle()

# Create obstacle_sprites group
obstacles_sprites = pygame.sprite.Group()
obstacle = Obstacles(50, 50)  # instantiate
# self, x_pos, y_pos, surf/display_surface, groups
# Obstacles(50, 50)
pygame.sprite.Group.add(obstacle)  # add instantiation
all_sprites.add(obstacle)  # do I pass in obstacle or obstacles??

# Player image, coordinates, and speed
start_health = 100
player = Player(WINDOW_WIDTH, WINDOW_HEIGHT, start_health, all_sprites, projectiles)
all_sprites.add(player)
player_sprite.add(player)

# Player score variable
score_sprite = pygame.sprite.GroupSingle()
score = TextDisplay(screen_location=(WINDOW_WIDTH / 2, 50), label='Score', data=0)
score_sprite.add(score)

money_sprite = pygame.sprite.GroupSingle()
money = TextDisplay(screen_location=(WINDOW_WIDTH / 2, 80), label='Money', data=0)
money_sprite.add(money)

# Create enemy spawner class to track enemies and enemy spawn
enemy_spawner = EnemySpawner(display_surface, player, 3, all_sprites)
enemy_sprites = enemy_spawner.enemy_sprite_group
enemy_projectiles = enemy_spawner.enemy_projectiles
exploding_enemies = enemy_spawner.exploding_enemies

# Make background surface
# background_surf = pygame.image.load('Assets/background/sand-arena-background.png').convert_alpha()
# background_surf = pygame.transform.scale(background_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))

# initialize data for background map
tmx_data = load_pygame('Assets/background/maps/EPICRPGWorldPackCryptV.1.3/crypt.tmx')


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # self.offset.x = player.rect.centerx - self.half_width
        # self.offset.y = player.rect.centery - self.half_height
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)


sprite_group = CameraGroup()

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            Tile(pos=pos, surf=surf, groups=(sprite_group,))

for obj in tmx_data.objects:
    pos = obj.x, obj.y
    if obj.image:
        Tile(pos=pos, surf=obj.image, groups=(sprite_group,))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.change_health(-20)
        '''

    # Update surfaces
    # display_surface.blit(background_surf, (0, 0))
    sprite_group.custom_draw(player)

    # Update and draw sprites
    all_sprites.draw(display_surface)
    all_sprites.update()

    # Update and draw enemies using spawner
    enemy_spawner.update()

    # Update and draw score text
    score_sprite.draw(display_surface)
    score_sprite.update()

    # Update and draw money text
    money_sprite.draw(display_surface)
    money_sprite.update()
    money.data = player.money
    money.update()

    # Update and draw explosions
    explosion_sprites.update()
    for explosion in explosion_sprites:
        display_surface.blit(explosion.image, explosion.rect)

    # Update and draw obstacles
    obstacles_sprites.update()
    for obstacles in obstacles_sprites:
        display_surface.blit(obstacles.image, obstacles.rect)
        obstacles.draw_obstacle()

    # (Logic for player collision with obstacles - might have to do this in player.py)
    # for obstacles in obstacles_sprites:
    #    if pygame.sprite.spritecollideany(player, obstacles):
    #        # some code

    # (Logic for enemy collision with obstacles - might have to do this in enemy.py, or do it below on 211)
    # for obstacles in obstacles_sprites:
    # if pygame.sprite.spritecollideany(enemy, obstacles):
    #        # some code

    # Draw a rect. Pass in display, color, xy width and height, player health, and height
    if player.health > 0:
        player.draw_healthbar(display_surface)

    for projectile in projectiles:
        projectile.update()

        if projectile.rect.right < 0:
            projectile.kill()

    for enemy in enemy_sprites:

        # # Allow for constant enemy movement
        # enemy.enemy_x += enemy.speed
        # enemy.enemy_y += enemy.speed

        for projectile in projectiles:
            # Check if the projectile has already hit an enemy the maximum number of times
            if projectile.hit_count == projectile.max_hits:
                continue

            # Check if the projectile collides with the enemy
            if pygame.sprite.collide_rect(projectile, enemy):
                # Check if the projectile has hit the enemy for the first time
                if not projectile.has_hit(enemy):
                    # Apply damage to the enemy
                    killed_enemy = enemy.change_health(-player.damage)

                    # Make explosion where the projectile is
                    explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                    explosion_sprites.add(explosion)

                    # play enemy damage sound
                    main_loop_sounds(0)

                    # Update the projectile's hit count and mark the enemy as hit by the projectile
                    projectile.hit_count += 1
                    projectile.mark_hit(enemy)

                    if killed_enemy:
                        score.data += 10
                        money.data += 10
                        player.money += 10

                        # play enemy death sound
                        main_loop_sounds(2)

                # Check if the projectile has hit the enemy the maximum number of times
                if projectile.hit_count == projectile.max_hits:
                    projectile.kill()

                # Only process the first enemy that collides with a projectile
                break

        if pygame.sprite.spritecollideany(enemy, player_sprite):
            enemy.move_back_from_player()
            player.change_health(-10)
            main_loop_sounds(1)

        for enemy_projectile in enemy_projectiles:
            if pygame.sprite.spritecollideany(enemy_projectile, player_sprite):
                enemy_projectile.kill()
                player.change_health(-20)
                main_loop_sounds(1)

        for exploding_enemy in exploding_enemies:
            if pygame.sprite.spritecollideany(exploding_enemy, player_sprite):
                player.change_health(-50)
                main_loop_sounds(1)
                exploding_enemy.kill()

        enemy.draw_healthbar(display_surface)

    projectiles.draw(display_surface)

    # Update display
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)

# End the game
pygame.quit()

