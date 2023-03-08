import pygame
from support import import_folder

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

class House(StaticTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,pygame.image.load('graphics/decoration/9 House/1.png').convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))

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
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, shift):
        self.rect.x += shift
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
    
    def play(self):
        self.playing = True
        self.current_frame = 0  # reset the current frame to the beginning of the animation

class PlayerSprite(AnimatedSprite):
    def __init__(self, size, x, y, frames):
        super().__init__(size, x, y, frames, "graphics/character/Owlet_Monster_Idle_4.png", 10)

class Coin(AnimatedSprite):
    def __init__(self, size, x, y, frames):
        super().__init__(size, x, y, frames, "graphics/coins/Coin.png", 10)

class MIAnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >+ len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self, shift):
        self.animate()
        self.rect.x += shift

class MICoin(MIAnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))