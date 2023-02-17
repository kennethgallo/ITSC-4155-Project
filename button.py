import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, text, text_color, background_color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(background_color)
        self.rect = self.image.get_rect()

        font = pygame.font.Font(None, 30)
        text = font.render(text, True, text_color, background_color)
        text_rect = text.get_rect(center=(width / 2, height / 2))
        self.image.blit(text, text_rect)

        self.text = text
        self.width = width
        self.height = height
