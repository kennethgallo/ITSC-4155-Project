import pygame

# Initialize pygame
pygame.init()

# load in each sound effect
enemy_damage = pygame.mixer.Sound('Music/enemy-damage.mp3')
player_damage = pygame.mixer.Sound('Music/player-damage.mp3')
new_round = pygame.mixer.Sound('Music/new-round.mp3')
player_death = pygame.mixer.Sound('Music/player-death.mp3')
projectile_sfx = pygame.mixer.Sound('Music/lazer.mp3')

# set the volume for each sound effect
master_volume = 0.1

enemy_damage.set_volume(master_volume)
player_damage.set_volume(master_volume)
new_round.set_volume(master_volume)
player_death.set_volume(master_volume)
projectile_sfx.set_volume(master_volume)


def main_loop_sounds(x):
    # enemy damage
    if x == 0:
        enemy_damage.play(0)

    # player damage
    if x == 1:
        player_damage.play(0)

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
    new_round.play(0)


def player_death_sound():
    player_death.play(0)


def projectile_sound():
    projectile_sfx.play(0)



