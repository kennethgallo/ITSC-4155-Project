import pygame

# Initialize pygame
pygame.init()

# Create display surface
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()

# Music by Kim Lightyear from Pixaby
pygame.mixer.music.load('Music/bg-song.mp3')
pygame.mixer.music.play(-1, 0.0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    pygame.display.update()

# End the game
pygame.quit()
