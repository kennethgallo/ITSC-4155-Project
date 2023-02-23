import pygame
from player import Player

# Initialize pygame
pygame.init()

# Create display surface
# display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_surface = pygame.display.set_mode((600, 600))
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# player_health = 150
player_health = 200

# set FPS and clock (allows for controlling movement speed regardless of machine speed)
# FPS can be changed to update movement of the character if needed
FPS = 60
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    clock.tick(60)
    display_surface.fill(black)

    #Draw a rect. Pass in display, color, xy width and height, player health, and height
    pygame.draw.rect(display_surface, red, (200, 250, 200, 5))

    pygame.draw.rect(display_surface, green, (200, 250, (player_health//2), 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            # End the game
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            player_health -= 5

    # Update display
    pygame.display.update()
