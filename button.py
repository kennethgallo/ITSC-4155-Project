import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, text, size):
        super().__init__()
        self.image = pygame.Surface((300, 100))
        self.image.fill('Blue')
        font = pygame.font.Font(None, 30)
        text = font.render(text, True, (0, 0, 0), (255, 255, 255))
        self.rect = self.image.get_rect()
        self.image.blit(text, self.rect.center)
        self.text = text
        self.size = size
