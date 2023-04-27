import pygame


class TextDisplay(pygame.sprite.Sprite):
    def __init__(self, screen_location, label, data, font_size):
        super().__init__()

        self.label = label
        self.data = data
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)

        # Set up text image
        self.text = ''
        self.setup_text()

        self.alias = True
        self.text_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.image = self.font.render(self.text, self.alias, self.text_color, self.bg_color)

        # Set up sprite rect
        self.center_location = screen_location
        self.rect = self.image.get_rect(center=self.center_location)

    def setup_text(self):
        if self.data is not None:
            self.text = str(self.label) + ': ' + str(self.data)
        else:
            self.text = str(self.label)

    def update(self):
        # Recreate sprite according to new score
        self.font = pygame.font.Font(None, self.font_size)
        self.setup_text()
        self.image = self.font.render(self.text, self.alias, self.text_color, self.bg_color)
        self.rect = self.image.get_rect(center=self.center_location)
