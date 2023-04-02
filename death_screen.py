import pygame
import sys


class DeathScreen:
    def __init__(self, player):
        self.player = player

    def display(self, screen):
        font = pygame.font.Font(None, 30)
        header = font.render("YOU DIED", True, (255, 0, 0))
        screen.blit(header, (300, 50))

    def run_display(self):
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        death_display = True
        while death_display:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    False
                    pygame.quit()
                    sys.exit()

            # Draw menu and update display
            screen.fill((0, 0, 0))
            self.display(screen)
            pygame.display.flip()
            clock.tick(60)
