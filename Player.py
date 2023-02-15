import pygame

# Create display surface
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.player_y = 0
        self.player_x = 0
        self.speed = 2

    def key_movement(self):
        # Find keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 0:
            self.player_y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.player_y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.player_x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.player_x += self.speed

        # Update rect values
        self.rect.x += self.player_x
        self.rect.y += self.player_y

        # Reset movement for next time
        self.player_x = 0
        self.player_y = 0

    def update(self):
        self.key_movement()
