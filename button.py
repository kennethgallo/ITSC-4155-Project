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


class ShopButton(pygame.sprite.Sprite):
    def __init__(self, upgrade_string, cost_string):
        self.width = 200
        self.height = 90

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        font = pygame.font.Font(None, 30)
        upgrade_text = font.render(upgrade_string, True, (100, 100, 100), (255, 255, 255))
        upgrade_text_rect = upgrade_text.get_rect(center=(self.width / 2, 30))

        cost_text = font.render(cost_string, True, (100, 100, 100), (255, 255, 255))
        cost_text_rect = cost_text.get_rect(center=(self.width / 2, 60))

        self.image.blit(upgrade_text, upgrade_text_rect)
        self.image.blit(cost_text, cost_text_rect)

        self.upgrade_string = upgrade_string
        self.cost_string = cost_string
