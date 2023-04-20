import pygame


def load_image(name, colorkey=False):
    """This function allows you to load images from the data folder."""
    image = pygame.image.load(name)
    if colorkey:
        image = pygame.transform.scale(image, SCREEN_SIZE)
    # image = image.convert_alpha()
    return image


tile_width = tile_height = 25
SCREEN_SIZE = (1024, 760)

tile_images = {'#': pygame.transform.scale(load_image('data/Map/ground.png'), (tile_width, tile_height)),
               '%': pygame.transform.scale(load_image('data/Map/grass.png'), (tile_width, tile_height)),
               '{': pygame.transform.scale(load_image('data/Map/stone.png'), (tile_width, tile_height)),
               '*': pygame.transform.scale(load_image('data/Map/foliage.png'), (tile_width, tile_height)),
               '/': pygame.transform.scale(load_image('data/Map/trunk.png'), (tile_width, tile_height)),
               '^': pygame.transform.scale(load_image('data/Map/sand.jpg'), (tile_width, tile_height)),
               '$': pygame.transform.scale(load_image('data/Map/snow.png'), (tile_width, tile_height)),
               'sword_left': load_image('data/Player/left_sword.png'),
               'sword': load_image('data/Player/sword.png')}


