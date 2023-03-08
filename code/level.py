import pygame
from support import import_csv_layout, import_cut_graphics
from settings import *
from tiles import Tile, House, StaticTile, MICoin, AnimatedSprite, Coin
from background import Background
from enemy import Enemy
from set_dressing import Sky, Water, Clouds
from player import Player


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        self.background = Background(surface)

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(
            terrain_layout, 'terrain')

        # decoration setup
        decoration_layout = import_csv_layout(level_data['decoration'])
        self.decoration_sprites = self.create_tile_group(
            decoration_layout, 'decoration')

        # coin setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # multiple image animation practice
        mi_coin_layout = import_csv_layout(level_data['mi_coins'])
        self.mi_coin_sprites = self.create_tile_group(
            mi_coin_layout, 'mi_coins')

        # foreground trees
        fg_trees_layout = import_csv_layout(level_data['fg_trees'])
        self.fg_tree_sprites = self.create_tile_group(
            fg_trees_layout, 'fg_trees')

        # grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # background trees
        bg_trees_layout = import_csv_layout(level_data['bg_trees'])
        self.bg_tree_sprites = self.create_tile_group(
            bg_trees_layout, 'bg_trees')

        # house
        house_layout = import_csv_layout(level_data['house'])
        self.house_sprites = self.create_tile_group(house_layout, 'house')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(
            constraint_layout, 'constraints')

        # alt sky
        # self.sky = Sky(18)

        # water
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 15, (level_width * 2))
        self.clouds = Clouds(400, level_width, 10)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(
                            'graphics/terrain/Tileset.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'decoration':
                        decoration_tile_list = import_cut_graphics(
                            'graphics/terrain/Tileset.png')
                        tile_surface = decoration_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'coins':
                        sprite = Coin(tile_size, x, y, 4)

                    if type == 'mi_coins':
                        sprite = MICoin(tile_size, x, y,
                                        'graphics/coins/multi_image_coins')

                    if type == 'fg_trees':
                        fg_trees_tile_list = import_cut_graphics(
                            'graphics/terrain/Tileset.png')
                        tile_surface = fg_trees_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'bg_trees':
                        bg_trees_tile_list = import_cut_graphics(
                            'graphics/terrain/Tileset.png')
                        tile_surface = bg_trees_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics(
                            'graphics/decoration/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'house':
                        sprite = House(tile_size, x, y)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface)
                    self.player.add(sprite)

                if val == '1':
                    image_path = 'graphics/character/Flag.png'
                    sprite = AnimatedSprite(tile_size, x, y, 4, image_path, 10)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites(
        )
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def run(self):
        # run the entire game / level

        # background
        self.background.update(self.world_shift)

        # alt sky
        # self.sky.draw(self.display_surface)
        # clouds
        self.clouds.draw(self.display_surface, self.world_shift)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # coin
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # mi_coins
        self.mi_coin_sprites.update(self.world_shift)
        self.mi_coin_sprites.draw(self.display_surface)

        # bg_trees
        self.bg_tree_sprites.update(self.world_shift)
        self.bg_tree_sprites.draw(self.display_surface)

        # decoration
        self.decoration_sprites.update(self.world_shift)
        self.decoration_sprites.draw(self.display_surface)

        # enemies
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # fg_trees
        self.fg_tree_sprites.update(self.world_shift)
        self.fg_tree_sprites.draw(self.display_surface)

        # house
        self.house_sprites.update(self.world_shift)
        self.house_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        # self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)

    def shift_world(self, shift_x):
        self.world_shift += shift_x
