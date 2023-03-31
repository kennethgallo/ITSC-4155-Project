import pygame
import threading
import time
import random
from enemy import Enemy
from text_display import TextDisplay


class EnemySpawner:
    def __init__(self, display_surface, player, max_rounds):
        self.display_surface = display_surface
        self.player = player
        self.max_rounds = max_rounds

        self.round = 1
        self.round_display = TextDisplay((100, 100), 'Round', self.round)
        self.round_sprite = pygame.sprite.GroupSingle()
        self.round_sprite.add(self.round_display)

        self.seconds_delay_between_enemies = 1
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
        num_enemies = curr_round * 4  # four enemies more each round for now

        for index in range(num_enemies):
            try:
                window_dimensions = pygame.display.get_window_size()
            except:
                print('game stopped, returning thread')
                return

            window_width = window_dimensions[0]
            window_height = window_dimensions[1]

            if direction == 0:
                x_pos = random.randrange(0, window_width)
                y_pos = -50
            elif direction == 1:
                x_pos = window_width + 50
                y_pos = random.randrange(0, window_height)
            elif direction == 2:
                x_pos = random.randrange(0, window_width)
                y_pos = window_height + 50
            else:
                x_pos = -50
                y_pos = random.randrange(0, window_height)

            # rotate direction
            direction += 1
            if direction > 3:
                direction = 0

            # create and add new enemy
            enemy = Enemy(index, 50 * curr_round, x_pos, y_pos)
            self.enemy_sprite_group.add(enemy)

            # delay the thread so the enemies have time between spawning
            time.sleep(self.seconds_delay_between_enemies)

    def update(self):
        self.enemy_sprite_group.draw(self.display_surface)
        self.enemy_sprite_group.update(self.player, self.enemy_sprite_group)

        if len(self.enemy_sprite_group) == 0:
            print(f'Round {self.round} over, starting round {self.round + 1}')

            self.round += 1
            self.round_display.data = self.round

            if self.round <= self.max_rounds:
                self.start_spawn_thread()
            else:
                print(f'All rounds beat! Total rounds: {self.max_rounds}')

        self.round_sprite.draw(self.display_surface)
        self.round_sprite.update()
