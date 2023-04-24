import sys
import pygame
import random
from pytmx.util_pygame import load_pygame

import sounds
from main_menu import MainMenu
from player import Player
from button import Button
from text_display import TextDisplay
from enemy_spawn import EnemySpawner
from tile import Tile
from explosion import Explosion
from sounds import main_loop_sounds
from obstacles import Obstacles
from item_drops import roll_drop, ItemDrop

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

# Main menu loop
main_menu = MainMenu(WINDOW_WIDTH, WINDOW_HEIGHT, display_surface, clock, FPS)
keep_menu = True
while keep_menu:
    keep_menu = main_menu.menu_loop()

# Create sprite groups
all_sprites = pygame.sprite.Group()
explosion_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
player_sprite = pygame.sprite.GroupSingle()
item_drops = pygame.sprite.Group()
obstacles_sprites = pygame.sprite.Group()

obstacle = Obstacles(50, 50)  # instantiate obstacle
# self, x_pos, y_pos, surf/display_surface, groups
# Obstacles(50, 50)
pygame.sprite.Group.add(obstacle)
all_sprites.add(obstacle)

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

# get dimensions of the map
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

# create a rectangle around the edge of the map
boundary_rect = pygame.Rect(0, 0, map_width, map_height)
boundary_rect.inflate_ip(-tmx_data.tilewidth, -tmx_data.tileheight)

# generate a random position
player_pos = pygame.math.Vector2(random.randint(boundary_rect.left, boundary_rect.right),
                                 random.randint(boundary_rect.top, boundary_rect.bottom))

# start player in random place
player.rect.center = player_pos


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.last_player_x = player.rect.centerx
        self.last_player_y = player.rect.centery

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        tiles = self.sprites()
        other_sprites = list(enemy_sprites) + list(enemy_projectiles) \
                        + list(explosion_sprites) + list(obstacles_sprites) \
                        + list(projectiles) + list(item_drops)

        for sprite in tiles + other_sprites:
            if isinstance(sprite, Tile):
                offset_pos = sprite.rect.topleft - self.offset
                display_surface.blit(sprite.image, offset_pos)
            else:
                offset_x = player.rect.centerx - self.last_player_x
                offset_y = player.rect.centery - self.last_player_y
                sprite.rect.centerx -= offset_x
                sprite.rect.centery -= offset_y

        self.last_player_x = player.rect.centerx
        self.last_player_y = player.rect.centery


sprite_group = CameraGroup()
wall_group = pygame.sprite.Group()

# cycle through all layers
walls = []
for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            Tile(pos=pos, surf=surf, groups=(sprite_group,))
    if layer.name.startswith('wall-'):
        for x, y, gid, in layer:
            rect = pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight)
            walls.append(rect)
            wall_sprite = pygame.sprite.Sprite(wall_group)
            wall_sprite.rect = rect

    # elif hasattr(layer, 'data'):
    #     for x, y, surf in layer.tiles():
    #         pos = (x * tmx_data.tilewidth, y * tmx_data.tileheight)
    #         tile_sprite = Tile(pos=pos, surf=surf, groups=(sprite_group,))

for obj in tmx_data.objects:
    pos = obj.x, obj.y
    if obj.image:
        Tile(pos=pos, surf=obj.image, groups=(sprite_group,))

# Main game loop
running = True
while running:
    display_surface.fill(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.change_health(-20)
        '''
    # calculate delta time
    # dt = clock.tick(60) / 1000.0  # 60 is the desired frame rate

    # Update player
    # player.update(dt, boundary_rect)

    # Update surfaces
    # display_surface.blit(display_surface, (0, 0))
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

                        # roll to see if an item should drop
                        roll = roll_drop()
                        if roll is not None:
                            item_drop = ItemDrop(roll, enemy.rect.center)
                            item_drops.add(item_drop)
                            all_sprites.add(item_drop)

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
                player.change_health(-15)
                main_loop_sounds(1)
                explosion = Explosion(exploding_enemy.rect.centerx, exploding_enemy.rect.centery)
                explosion_sprites.add(explosion)
                exploding_enemy.kill()

        enemy.draw_healthbar(display_surface)

    if len(item_drops) > 0:
        for drop in item_drops:
            if pygame.sprite.spritecollideany(drop, player_sprite):
                if drop.item_type == 'health':
                    player.change_health(25)
                elif drop.item_type == 'money':
                    player.money += 25
                drop.kill()

    projectiles.draw(display_surface)

    # check for collisions with walls
    for wall in wall_group:
        if pygame.sprite.collide_rect(player, wall):
            print('Collision detected!')

    # update sprites
    sprite_group.update()

    # Update display
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)

# End the game
pygame.quit()
