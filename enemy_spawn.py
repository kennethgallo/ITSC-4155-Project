import pygame
from enemy import Enemy

enemy_spawn_points = [
    (100, 100),
    (200, 300),
    (25, 600),
    (700, 400),
    (500, 200),
    (400, 650),
    (300, 50)
]

class EnemySpawner():
    def __init__(self, display_surface, player):
        self.display_surface = display_surface
        self.player = player
        self.round = 1
        self.delay_between_enemies = 1000
        self.enemy_sprite_group = pygame.sprite.Group()
        for index in range(len(enemy_spawn_points)):
            x_pos = enemy_spawn_points[index][0]
            y_pos = enemy_spawn_points[index][1]
            enemy = Enemy(index, 100 * self.round, x_pos, y_pos)
            self.enemy_sprite_group.add(enemy)

    def update(self):
        self.enemy_sprite_group.draw(self.display_surface)
        self.enemy_sprite_group.update(self.player, self.enemy_sprite_group)
