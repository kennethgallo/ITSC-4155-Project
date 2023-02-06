import pygame

# Initialize pygame
pygame.init()

# Create display surface
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

# End the game
pygame.quit()
