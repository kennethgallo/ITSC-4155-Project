import pygame

# Initialize pygame
pygame.init()

# Create display surface
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()

# Music by Kim Lightyear from Pixaby
pygame.mixer.music.load('Music/bg-song.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.05)

# Make background surface
background_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background_surf.fill(color='white')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    display_surface.blit(background_surf, (0, 0))
    pygame.display.update()

# End the game
pygame.quit()
