import pygame
from Images import tile_images, tile_height, tile_width

tiles_group = pygame.sprite.Group()


class Map:
    """This class is responsible for updating the map: structure and destruction."""

    def __init__(self, level):
        self.map = []
        map_file = open(level)
        for i in map_file:
            self.map.append(list(i.strip()))
        self.info_destroy = [0, 0, 0]
        self.info_create = [0, 0, 0]
        self.ly = len(self.map)
        self.lx = len(self.map[0])


class Tile(pygame.sprite.Sprite):
    """This sprite class contains all map blocks."""

    def __init__(self, tile_type, pos_x, pos_y, x, y, tiles_group, all_sprites, f=0):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type
        self.pos_x = x
        self.pos_y = y
        if f:
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            print(tile_type)
        else:
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
