import pygame
import threading
import time
import random
from enemy import Enemy
from boss import Boss
from text_display import TextDisplay
from sounds import new_round_sound


class EnemySpawner:
    def __init__(self, display_surface, player, max_rounds, all_sprites):
        self.display_surface = display_surface
        self.player = player
        self.max_rounds = 4
        self.game_over = False

        self.all_sprites = all_sprites
        self.enemy_projectiles = pygame.sprite.Group()
        self.exploding_enemies = pygame.sprite.Group()

        self.round = 1
        self.num_enemies_per_round = 8
        self.round_display = TextDisplay((100, 100), 'Round', self.round, 50)
        self.round_sprite = pygame.sprite.GroupSingle()
        self.round_sprite.add(self.round_display)

        self.seconds_delay_between_enemies = 2
        self.enemy_sprite_group = pygame.sprite.Group()
        self.start_spawn_thread()

    # Start separate thread for timed enemy spawning;
    #   A separate thread is necessary so that the delay
    #   will not stop the main thread
    def start_spawn_thread(self):
        spawn_thread = threading.Thread(target=self.spawn_enemies, args=(self.round_display.data,))
        spawn_thread.start()

    def spawn_enemies(self, curr_round):
        direction = 0  # 0: north, 1: east, 2: south, 3: west

        if curr_round == 4:  # spawn boss on round 4
            boss = Boss(start_health=5000, x_pos=300, y_pos=100, all_sprites=self.all_sprites, enemy_projectiles=self.enemy_projectiles, image='Assets/enemy/enemy1.png', display_surface=self.display_surface)
            self.enemy_sprite_group.add(boss)
        else:
            num_enemies = curr_round * self.num_enemies_per_round  # six enemies more each round for now

            for index in range(num_enemies):
                try:
                    window_dimensions = pygame.display.get_window_size()
                except:
                    print('game stopped, returning thread')
                    return

                window_width = window_dimensions[0]
                window_height = window_dimensions[1]

                curr_enemy_in_loop = index % self.num_enemies_per_round
                if curr_enemy_in_loop >= 6:  # if last two enemies in loop of 6
                    enemy_type = 'projectile'
                elif curr_enemy_in_loop >= 4 and curr_enemy_in_loop < 6:
                    enemy_type = 'exploding'
                else:
                    enemy_type = 'melee'

                if direction == 0:  # North
                    x_pos = random.randrange(0, window_width)
                    if enemy_type != 'projectile':
                        y_pos = -50
                    else:
                        y_pos = 50

                elif direction == 1:  # East
                    if enemy_type != 'projectile':
                        x_pos = window_width + 50
                    else:
                        x_pos = window_width - 50
                    y_pos = random.randrange(0, window_height)

                elif direction == 2:  # South
                    x_pos = random.randrange(0, window_width)
                    if enemy_type != 'projectile':
                        y_pos = window_height + 50
                    else:
                        y_pos = window_height - 50

                else:  # West
                    if enemy_type != 'projectile':
                        x_pos = -50
                    else:
                        x_pos = 50
                    y_pos = random.randrange(0, window_height)

                # rotate direction
                direction += 1
                if direction > 3:
                    direction = 0

                # create and add new enemy
                enemy = Enemy(index, 50 * curr_round, x_pos, y_pos, self.all_sprites, self.enemy_projectiles, enemy_type)
                self.enemy_sprite_group.add(enemy)
                if enemy_type == 'exploding':
                    self.exploding_enemies.add(enemy)

                # delay the thread so the enemies have time between spawning
                time.sleep(self.seconds_delay_between_enemies)

    def update(self):
        self.enemy_sprite_group.draw(self.display_surface)
        self.enemy_sprite_group.update(self.player, self.enemy_sprite_group)

        if self.game_over:
            return

        if len(self.enemy_sprite_group) == 0:
            print(f'Round {self.round} over, starting round {self.round + 1}')

            self.round += 1
            self.round_display.data = self.round

            # Play new round sound
            new_round_sound()

            if self.round <= self.max_rounds:
                self.start_spawn_thread()
            else:
                print(f'All rounds beat! Total rounds: {self.max_rounds}')
                self.game_over = True

        self.round_sprite.draw(self.display_surface)
        self.round_sprite.update()
