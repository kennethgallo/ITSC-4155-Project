import pygame
from enemy_spawn import enemy_spawn_points


class Enemy(pygame.sprite.Sprite):
    def __init__(self, index, start_health):
        super().__init__()
        self.image = pygame.image.load('Assets/enemy/enemy1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.health = start_health
        self.rect.x = enemy_spawn_points[index][0]
        self.rect.y = enemy_spawn_points[index][1]
        self.max_speed = 5
        self.speed = self.max_speed
        self.vector = pygame.math.Vector2(0, 0)
        self.last_collision_time = pygame.time.get_ticks()

    def movement(self, player):
        # If moving away from the player, start moving back slowly
        if self.speed < self.max_speed:
            self.speed += 0.25
            if self.speed > self.max_speed:
                self.speed = self.max_speed

        # Create a direct vector from enemy to player coordinates
        self.vector = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        if self.vector.length() > 0:
            self.vector.normalize()
            # Move along this vector towards the player at current speed
            self.vector.scale_to_length(self.speed)
            self.rect.move_ip(self.vector)

    def move_back_from_player(self):
        self.speed = -5

    def change_health(self, amount):
        self.health += amount
        if self.health <= 0:
            self.kill()
            return True
        else:
            return False

    def check_collision(self, enemies):
        # Checks each enemy
        for enemy in enemies:

            # Makes sure it does not count itself
            if enemy != self:

                # Checks for collision then moves the enemy backwards first, then left and if it is still overlapping moves right (in the if statements)
                if self.rect.colliderect(enemy.rect):

                    # This basically checks who hit the other first and moves the first one
                    if self.last_collision_time > enemy.last_collision_time:
                        self.rect.move_ip(-self.vector)
                        self.rect.move_ip(pygame.math.Vector2(5, 0))

                        if any(self.rect.colliderect(e.rect) for e in enemies if e != self):
                            self.rect.move_ip(pygame.math.Vector2(-10, 0))
                        self.last_collision_time = pygame.time.get_ticks()

                    else:
                        enemy.rect.move_ip(-enemy.vector)  # move back the other enemy
                        enemy.rect.move_ip(pygame.math.Vector2(5, 0))  # move to the right
                        if any(enemy.rect.colliderect(e.rect) for e in enemies if e != enemy):
                            enemy.rect.move_ip(pygame.math.Vector2(-10, 0))  # move to the left if still overlapping
                        enemy.last_collision_time = pygame.time.get_ticks()

    def update(self, player, enemies):
        self.movement(player)
        # self.check_collision(enemies)
