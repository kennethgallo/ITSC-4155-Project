import sys
import pygame
from button import Button
import player



class WinScreen:
    def __init__(self, window_width, window_height, display_surface, final_score, enemies_defeated, final_time):
        self.display_surface = display_surface

        # Main menu surface
        self.background_surface = pygame.Surface((window_width, window_height))
        self.background_surface.fill('Black')

        # Text display
        self.title_font = pygame.font.Font(None, 50)
        self.title_text = self.title_font.render('CONGRATULATIONS, YOU WIN!', True, 'Green')
        self.title_rect = self.title_text.get_rect(center=(window_width / 2, 200))

        # Main menu buttons
        self.menu_buttons = pygame.sprite.Group()

        # Final time display
        self.timer_font = pygame.font.Font(None, 30)
        self.final_time = final_time
        self.timer_text = self.timer_font.render(f'Final Time: {self.final_time/1000} seconds', True, 'White')
        self.timer_rect = self.timer_text.get_rect(center=(window_width / 2, 300))

        # Enemies Defeated Display
        self.enemies_defeated_font = pygame.font.Font(None, 30)
        self.enemies_defeated = enemies_defeated
        self.enemies_defeated_text = self.enemies_defeated_font.render('Enemies Defeated: {}'.format(self.enemies_defeated), True, 'White')
        self.enemies_defeated_rect = self.enemies_defeated_text.get_rect(center=(window_width / 2, 350))

        # Final score display
        self.score_font = pygame.font.Font(None, 30)
        self.final_score = final_score - (final_time / 10000)
        self.score_text = self.score_font.render('Final Score: {}'.format(self.final_score), True, 'White')
        self.score_rect = self.score_text.get_rect(center=(window_width / 2, 400))

        # Quit button
        self.quit_button = Button('Quit', 'Black', 'White', 200, 100)
        self.quit_button.rect.center = (window_width / 2, 600)

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
        self.display_surface.blit(self.timer_text, self.timer_rect)
        self.display_surface.blit(self.enemies_defeated_text, self.enemies_defeated_rect)
        self.display_surface.blit(self.score_text, self.score_rect)
        self.menu_buttons.draw(self.display_surface)

        pygame.display.update()

        return True
