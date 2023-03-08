import pygame, sys
from settings import *
from level import Level
from game_data import level_0

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)
dt = 0  # Define the dt variable here

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('black')
    dt = clock.tick(60) / 1000.0  # Update the dt variable here
    level.run()  # Pass the dt variable to the run() method
    
    pygame.display.update()
    clock.tick(60)