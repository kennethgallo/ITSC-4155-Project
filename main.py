import pygame
from Player import Player

# Initialize pygame
pygame.init()

# Create display surface
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()

# Music by Kim Lightyear from Pixaby
pygame.mixer.music.load('Music/bg-song.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.01)

# set FPS and clock (allows for controlling movement speed regardless of machine speed)
# FPS can be changed to update movement of the character if needed
FPS = 60
clock = pygame.time.Clock()

# Player image, coordinates, and speed
player = pygame.sprite.GroupSingle()
player.add(Player())

# Make background surface
background_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background_surf.fill(color='white')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Update surfaces
    display_surface.blit(background_surf, (0, 0))

    # Update player
    player.draw(display_surface)
    player.update()

    # Update display
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)

# End the game
pygame.quit()
