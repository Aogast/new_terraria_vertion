from Persons import Person


class Player(Person):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.inventory = {'sword': 1}
        self.pos_x = tile_width * pos_x + 15
        self.pos_y = tile_height * pos_y + 5
        self.make_inventary()
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def make_inventary(self, coords=None):
        """Player inventory creation"""
        a = list(self.inventory.keys())
        if f == 0:
            for i in range(len(a)):
                Playerinventary(tile_images[a[i]], i * 40, 0, f)
        elif f == 1:
            for i in range(len(a)):
                Playerinventary(tile_images[a[i]], coords[i][0], coords[i][1], f)
        else:
            Playerinventary(f, len(a) * 40, 5, 1)



class Playerinventary(pygame.sprite.Sprite):
    """Hero inventory sprite class"""
    def __init__(self, image, pos_x, pos_y, f=0):
        super().__init__(inventory_group, all_sprites)
        self.image = pygame.transform.scale(image, (40, 40))
        if f:
            self.rect = self.image.get_rect().move(pos_x, pos_y)
        else:
            self.rect = self.image.get_rect().move(10 * pos_x + 5, 10 * pos_y + 5)