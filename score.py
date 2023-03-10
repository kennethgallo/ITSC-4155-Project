import pygame


class Score(pygame.sprite.Sprite):
    def __init__(self, window_width, score):
        super().__init__()

        self.score = score
        self.font = pygame.font.Font(None, 50)

        # Set up text image
        self.text = "Score: " + str(self.score)
        self.alias = True
        self.text_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.image = self.font.render(self.text, self.alias, self.text_color, self.bg_color)

        # Set up sprite rect
        self.center_location = (window_width / 2, self.image.get_height() + 10)
        self.rect = self.image.get_rect(center=self.center_location)

    def update_score(self, amount):
        self.score += amount

    def update(self):
        # Recreate sprite according to new score
        self.font = pygame.font.Font(None, 50)
        self.text = "Score: " + str(self.score)
        self.image = self.font.render(self.text, self.alias, self.text_color, self.bg_color)
        self.rect = self.image.get_rect(center=self.center_location)
