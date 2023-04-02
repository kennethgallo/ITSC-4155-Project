import pygame

# Initialize pygame
pygame.init()

# set volume for all sounds
pygame.mixer.music.set_volume(0.5)


def main_loop_sounds(x):
    # enemy damage
    if x == 0:
        pygame.mixer.music.load('Music/enemy-damage.mp3')
        pygame.mixer.music.play(0)

    '''
    # enemy death
    if x == 1:
        pygame.mixer.music.load('Music/enemy-death.mp3')
        pygame.mixer.music.play(0)
        
    # player damage
    if x == 2:
        pygame.mixer.music.load('Music/enemy-damage.mp3')
        pygame.mixer.music.play(0)
    '''


def new_round_sound():
    pygame.mixer.music.load('Music/new-round.mp3')
    pygame.mixer.music.play(0)


def player_death_sound():
    pygame.mixer.music.load('Music/player-death.mp3')
    pygame.mixer.music.play(0)


def projectile_sound():
    pygame.mixer.music.load('Music/lazer.mp3')
    pygame.mixer.music.play(0)



