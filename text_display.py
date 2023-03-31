import pygame


class TextDisplay(pygame.sprite.Sprite):
    def __init__(self, screen_location, label, data):
        super().__init__()

        self.label = label
        self.data = data
        self.data = data
        self.font = pygame.font.Font(None, 50)

        # Set up text image
        self.text = str(self.label) + ': ' + str(self.data)
        self.alias = True
        self.text_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.image = self.font.render(self.text, self.alias, self.text_color, self.bg_color)

        # Set up sprite rect
        self.center_location = screen_location
        self.rect = self.image.get_rect(center=self.center_location)

    def update(self):
        # Recreate sprite according to new score
        self.font = pygame.font.Font(None, 50)
        self.text = str(self.label) + ': ' + str(self.data)
        self.image = self.font.render(self.text, self.alias, self.text_color, self.bg_color)
        self.rect = self.image.get_rect(center=self.center_location)
