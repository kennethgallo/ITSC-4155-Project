import sys
import pygame
from button import Button


class MainMenu:
    def __init__(self, window_width, window_height, display_surface, clock, FPS):
        self.display_surface = display_surface
        self.clock = clock
        self.FPS = FPS

        # Main menu surface
        self.background_surface = pygame.Surface((window_width, window_height))
        self.background_surface.fill('White')

        self.title_font = pygame.font.Font('Assets/fonts/Feral-Regular.ttf', 50)
        self.title_text = self.title_font.render('Creepy Crawlers', True, (0, 0, 255), (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(window_width / 2, 100))

        self.music_font = pygame.font.Font('Assets/fonts/Feral-Regular.ttf', 22)
        self.music_text = self.music_font.render('Music by Late Summerchild', True, (0, 0, 255), (255, 255, 255))
        self.music_rect = self.music_text.get_rect(center=(window_width / 4, 100))

        # Main menu buttons
        self.menu_buttons = pygame.sprite.Group()
        # Start button
        self.start_button = Button('Start', 'White', 'Black', 200, 100)
        self.start_button.rect.center = (window_width * (1 / 3), window_height / 2)
        # Quit button
        self.quit_button = Button('Quit', 'White', 'Black', 200, 100)
        self.quit_button.rect.center = (window_width * (2 / 3), window_height / 2)

        self.menu_buttons.add(self.start_button)
        self.menu_buttons.add(self.quit_button)

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
                if self.start_button.rect.collidepoint(mouse_pos):
                    return False
                elif self.quit_button.rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        self.display_surface.blit(self.background_surface, (0, 0))
        self.display_surface.blit(self.title_text, self.title_rect)
        self.display_surface.blit(self.music_text, self.music_rect)
        self.menu_buttons.draw(self.display_surface)

        pygame.display.update()
        self.clock.tick(self.FPS)

        return True
