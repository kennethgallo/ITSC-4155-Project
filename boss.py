import pygame
from enemy import Enemy

class Boss(pygame.sprite.Sprite):
    def __init__(self, start_health, x_pos, y_pos, all_sprites, enemy_projectiles, image, display_surface):
        super().__init__()

        self.display_surface = display_surface

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

        self.all_sprites = all_sprites
        self.enemy_projectiles = enemy_projectiles

        self.start_health = start_health
        self.health = self.start_health

        self.max_speed = 6
        self.speed = self.max_speed
        self.vector = pygame.math.Vector2(0, 0)
        self.last_collision_time = pygame.time.get_ticks()

        self.rect.x = x_pos
        self.rect.y = y_pos

        self.is_sprinting = False
        self.last_sprint_time = pygame.time.get_ticks()

    def movement(self, player):
        # Create a direct vector from enemy to player coordinates
        self.vector = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        # If moving away from the player, start moving back slowly
        if self.speed < self.max_speed:
            self.speed += 0.25
            if self.speed > self.max_speed:
                self.speed = self.max_speed

        # Move along this vector towards the player at current speed
        if self.vector.length() > 0:
            self.vector.normalize()
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

    def draw_healthbar(self, display_surface):
        red = (255, 0, 0)
        green = (0, 255, 0)

        barx = self.rect.x
        bary = self.rect.y

        background_length = 110
        foreground_length = (float(self.health) / float(self.start_health)) * background_length

        pygame.draw.rect(display_surface, red, (barx - 25, bary - 25, background_length, 10))
        pygame.draw.rect(display_surface, green, (barx - 25, bary - 25, foreground_length, 10))

    def sprint(self):
        self.speed = 12
        self.image = pygame.image.load('Assets/enemy/enemy2.png').convert_alpha()
        self.is_sprinting = True

    def check_collision(self, enemies):
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                if pygame.time.get_ticks() - enemy.last_collision_time > 1000:
                    enemy.last_collision_time = pygame.time.get_ticks()
                    enemy.change_health(-1)
                    self.change_health(1)

    def update(self, player, enemies):
        if self.is_sprinting:  # add this block to check if boss is sprinting
            current_time = pygame.time.get_ticks()
            if current_time - self.last_sprint_time > 2000:
                self.speed = 6
                self.image = pygame.image.load('Assets/enemy/enemy1.png').convert_alpha()
                self.is_sprinting = False
            else:
                self.movement(player)
                self.check_collision(enemies)
        else:
            self.movement(player)
            self.check_collision(enemies)

        # add this block to check if it's time to sprint
        current_time = pygame.time.get_ticks()
        if not self.is_sprinting and current_time - self.last_sprint_time > 6000:
            self.sprint()
            self.last_sprint_time = current_time