import sys
import pygame
from button import Button
import player



class DeathScreen:
    def __init__(self, window_width, window_height, display_surface):
        self.display_surface = display_surface

        # Main menu surface
        self.background_surface = pygame.Surface((window_width, window_height))
        self.background_surface.fill('Black')

        # Text display
        self.title_font = pygame.font.Font(None, 50)
        self.title_text = self.title_font.render('YOU DIED', True, 'Red')
        self.title_rect = self.title_text.get_rect(center=(window_width / 2, window_height / 4))

        # Main menu buttons
        self.menu_buttons = pygame.sprite.Group()

        # Final score display
        self.score_font = pygame.font.Font(None, 30)
        self.final_score = 0
        self.score_text = self.score_font.render('Final Score: {}'.format(self.final_score), True, 'White')
        self.score_rect = self.score_text.get_rect(center=(window_width / 2, window_height / 2))

        # Quit button
        self.quit_button = Button('Quit', 'Black', 'White', 200, 100)
        self.quit_button.rect.center = (window_width / 2, window_height * (3 / 4))

        self.menu_buttons.add(self.quit_button)

        self.test = False

    def menu_loop(self):
        pygame.mixer.music.load('Music/gameloop2.mp3')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.quit_button.rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


        self.display_surface.blit(self.background_surface, (0, 0))
        self.display_surface.blit(self.title_text, self.title_rect)
        self.display_surface.blit(self.score_text, self.score_rect)
        self.menu_buttons.draw(self.display_surface)

        pygame.display.update()

        return True
