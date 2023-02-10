import pygame

# Initialize pygame
pygame.init()

# Create display surface
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_window_size()

# Music by Kim Lightyear from Pixaby
pygame.mixer.music.load('Music/bg-song.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.01)

# Player image, coordinates, and speed
player = pygame.image.load('Assets/player.png')
player = pygame.transform.scale(player, (60, 60))
player_x = 0
player_y = 0
speed = 2

# Make background surface
background_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background_surf.fill(color='white')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= speed
    if keys[pygame.K_s]:
        player_y += speed
    if keys[pygame.K_a]:
        player_x -= speed
    if keys[pygame.K_d]:
        player_x += speed

    display_surface.blit(background_surf, (0, 0))
    display_surface.blit(player, (player_x, player_y))

    pygame.display.update()

# End the game
pygame.quit()
