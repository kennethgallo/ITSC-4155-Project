import sys
import pygame
from player import Player
from button import Button

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

# Main menu surface
menu_background_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
menu_background_surface.fill('White')

title_font = pygame.font.Font(None, 28)
title_text = title_font.render('Game Title Main Menu', True, (0, 0, 0), (255, 255, 255))
title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, 100))

# Main menu buttons
menu_buttons = pygame.sprite.Group()
# Start button
start_button = Button('Start', 'White', 'Black', 200, 100)
start_button.rect.center = (WINDOW_WIDTH * (1 / 3), WINDOW_HEIGHT / 2)
# Quit button
quit_button = Button('Quit', 'White', 'Black', 200, 100)
quit_button.rect.center = (WINDOW_WIDTH * (2 / 3), WINDOW_HEIGHT / 2)

menu_buttons.add(start_button)
menu_buttons.add(quit_button)


# Main menu loop
main_menu = True
while main_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            main_menu = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.rect.collidepoint(mouse_pos):
                main_menu = False
            elif quit_button.rect.collidepoint(mouse_pos):
                main_menu = False
                pygame.quit()
                sys.exit()

    display_surface.blit(menu_background_surface, (0, 0))
    display_surface.blit(title_text, title_rect)
    menu_buttons.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)


# Player image, coordinates, and speed
player = pygame.sprite.GroupSingle()
player.add(Player(WINDOW_WIDTH, WINDOW_HEIGHT))

# Make background surface
# background_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background_surf = pygame.image.load('Assets/background/sand-arena-background.png').convert_alpha()
background_surf = pygame.transform.scale(background_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))


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
