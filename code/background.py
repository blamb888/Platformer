import pygame
from settings import *

class Background:
    def __init__(self, surface):
        self.image = pygame.image.load('graphics/background/Background.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.rect = self.image.get_rect()
        self.surface = surface
        self.rect.x = 0
        self.rect.y = 0

    def update(self, shift_x):
        self.rect.x = -shift_x
        self.surface.blit(self.image, self.rect)

