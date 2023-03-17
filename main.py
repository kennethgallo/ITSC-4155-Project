import sys
import pygame
from pytmx.util_pygame import load_pygame
from player import Player
from enemy import Enemy
from button import Button
from score import Score
from enemy_spawn import enemy_spawn_points
from tile import Tile

# Initialize pygame
pygame.init()

# Create display surface
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()

# Music by Kim Lightyear from Pixaby
'''
pygame.mixer.music.load('Music/bg-song.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.01)
'''

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

# Create enemy_sprites group
enemy_sprites = pygame.sprite.Group()

# Create projectiles group
projectiles = pygame.sprite.Group()

player_sprite = pygame.sprite.GroupSingle()

# Player image, coordinates, and speed
start_health = 100
player = Player(WINDOW_WIDTH, WINDOW_HEIGHT, start_health, all_sprites, projectiles)
all_sprites.add(player)
player_sprite.add(player)

# Player score variable
score_sprite = pygame.sprite.GroupSingle()
score = Score(WINDOW_WIDTH, 0)
score_sprite.add(score)

# Add enemies to enemy sprite group
for x in range(len(enemy_spawn_points)):
    enemy_sprites.add(Enemy(x, start_health))

# health bar stuff
red = (255, 0, 0)
green = (0, 255, 0)

# Make background surface
# background_surf = pygame.image.load('Assets/background/sand-arena-background.png').convert_alpha()
# background_surf = pygame.transform.scale(background_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))

# initialize data for background map
tmx_data = load_pygame('Assets/background/maps/EPICRPGWorldPackCryptV.1.3/crypt.tmx')
sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            Tile(pos=pos, surf=surf, groups=sprite_group)

for obj in tmx_data.objects:
    pos = obj.x, obj.y
    if obj.image:
        Tile(pos=pos, surf=obj.image, groups=sprite_group)

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
    sprite_group.draw(display_surface)

    # Update and draw sprites
    all_sprites.draw(display_surface)
    all_sprites.update()

    # Update and draw enemies
    enemy_sprites.draw(display_surface)
    enemy_sprites.update(player)

    # Update and draw score text
    score_sprite.draw(display_surface)
    score_sprite.update()

    # Draw a rect. Pass in display, color, xy width and height, player health, and height
    if player.health > 0:
        pygame.draw.rect(display_surface, red, (player.rect.x - 25, player.rect.y - 25, start_health, 10))
        pygame.draw.rect(display_surface, green, (player.rect.x - 25, player.rect.y - 25, player.health, 10))

    for projectile in projectiles:
        projectile.update()
        if projectile.rect.right < 0:
            projectile.kill()

    for enemy in enemy_sprites:

        # # Allow for constant enemy movement
        # enemy.enemy_x += enemy.speed
        # enemy.enemy_y += enemy.speed

        if pygame.sprite.spritecollideany(enemy, projectiles):
            killed_enemy = enemy.change_health(-10)
            if killed_enemy:
                score.update_score(10)

        if pygame.sprite.spritecollideany(enemy, player_sprite):
            enemy.move_back_from_player()
            player.change_health(-1)

        pygame.draw.rect(display_surface, red, (enemy.rect.x - 25, enemy.rect.y - 25, start_health, 10))
        pygame.draw.rect(display_surface, green, (enemy.rect.x - 25, enemy.rect.y - 25, enemy.health, 10))

    projectiles.draw(display_surface)

    # Update display
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)

# End the game
pygame.quit()
