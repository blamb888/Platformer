import pygame
from support import import_csv_layout, import_cut_graphics
from settings import *
from tiles import StaticTile, MICoin, Coin
from background import Background


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = -1
        
        self.background = Background(surface)
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # decoration setup
        decoration_layout = import_csv_layout(level_data['decoration'])
        self.decoration_sprites = self.create_tile_group(decoration_layout, 'decoration')

        # coin setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        
        # multiple image animation practice
        mi_coin_layout = import_csv_layout(level_data['mi_coins'])
        self.mi_coin_sprites = self.create_tile_group(mi_coin_layout, 'mi_coins')
        
        # foreground trees
        fg_trees = import_csv_layout(level_data['fg_trees'])
        self.mi_coin_sprites = self.create_tile_group(fg_trees, 'fg_trees')
        
        # background trees
        bg_trees = import_csv_layout(level_data['bg_trees'])
        self.mi_coin_sprites = self.create_tile_group(bg_trees, 'bg_trees')
        
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/terrain/Tileset.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'decoration':
                        decoration_tile_list = import_cut_graphics('graphics/terrain/Tileset.png')
                        tile_surface = decoration_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    
                    if type == 'coins':
                        sprite = Coin(tile_size, x, y, 4)
                    
                    if type == 'mi_coins':
                        sprite = MICoin(tile_size, x, y, 'graphics/coins/multi_image_coins')
                    
                    if type == 'fg_trees':
                        fg_trees_tile_list = import_cut_graphics('graphics/terrain/Tileset.png')
                        tile_surface = fg_trees_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    
                    if type == 'bg_trees':
                        bg_trees_tile_list = import_cut_graphics('graphics/terrain/Tileset.png')
                        tile_surface = bg_trees_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    sprite_group.add(sprite)
                    
        return sprite_group
    
    def run(self):
        # run the entire game / level
        
        # background
        self.background.update(self.world_shift)
        
        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # decoration
        self.decoration_sprites.update(self.world_shift)
        self.decoration_sprites.draw(self.display_surface)
        
        # coin
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        
        # mi_coins
        self.mi_coin_sprites.update(self.world_shift)
        self.mi_coin_sprites.draw(self.display_surface)
    
    def shift_world(self, shift_x):
        self.world_shift += shift_x