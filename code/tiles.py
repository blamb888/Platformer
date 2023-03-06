import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,size, x, y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, shift):
        self.rect.x += shift
        
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, size, x, y, frames, image_path, animation_speed):
        super().__init__()
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.images = []
        self.sheet_width, self.sheet_height = self.sheet.get_size()
        self.frame_width = self.sheet_width // frames
        self.frame_height = self.sheet_height
        for i in range(frames):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sheet, (0, 0), rect)
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
            self.images.append(image)
        self.index = 0
        self.image = self.images[self.index]
        self.animation_speed = animation_speed
        self.counter = 0
        self.rect = self.image.get_rect(center=(x + size // 2, y + size // 2))  # use center position

    def update(self, shift):
        self.rect.x += shift
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

class Coin(AnimatedSprite):
    def __init__(self, size, x, y, frames):
        super().__init__(size, x, y, frames, "graphics/coins/Coin.png", 10)
