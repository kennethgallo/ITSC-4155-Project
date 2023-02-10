import pygame


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
        if keys[pygame.K_w]:
            self.player_y -= self.speed
        if keys[pygame.K_s]:
            self.player_y += self.speed
        if keys[pygame.K_a]:
            self.player_x -= self.speed
        if keys[pygame.K_d]:
            self.player_x += self.speed

        # Update rect values
        self.rect.x += self.player_x
        self.rect.y += self.player_y

        # Reset movement for next time
        self.player_x = 0
        self.player_y = 0

    def update(self):
        self.key_movement()
