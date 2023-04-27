import pygame
from Images import tile_images


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.gravity = 3
        self.speed_gravity = 1
        self.inventory = {'sword': 1}
        self.health = 100
        self.current_item_index = 0
        self.inventory_index = 0
        self.jump_power = 25
        self.is_jump = False
        self.speed = 5
        self.damage = 10
        self.frames_right = [pygame.image.load("data/Player/right_player.png"),
                             pygame.image.load("data/Player/right2.png"),
                             pygame.image.load("data/Player/right3.png"),
                             pygame.image.load("data/Player/right_player.png")]
        self.frames_left = [pygame.image.load("data/Player/sprite1.png"),
                            pygame.image.load("data/Player/sprite2.png"),
                            pygame.image.load("data/Player/sprite3.png"),
                            pygame.image.load("data/Player/player.png")]
        for img in range(4):
            self.frames_left[img] = pygame.transform.scale(self.frames_left[img], (25, 45))
            self.frames_right[img] = pygame.transform.scale(self.frames_right[img], (25, 45))
        self.image = self.frames_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = "right"
        self.sword_image = pygame.image.load("data/Player/sword.png")

    def get_down(self):
        self.rect.y += self.gravity
        if self.gravity < 15:
            self.gravity += self.speed_gravity
            self.speed_gravity += 1

    def update_right(self):
        self.current_item_index += 1
        self.current_item_index %= 4
        self.image = self.frames_right[self.current_item_index]

    def update_left(self):
        self.current_item_index += 1
        self.current_item_index %= 4
        self.image = self.frames_left[self.current_item_index]

    def update(self):
        self.current_item_index = 0
        if self.direction == "left":
            self.image = self.frames_left[3]

        else:
            self.image = self.frames_right[0]

    def jump(self):
        self.rect.y -= self.jump_power
        if self.jump_power > 10:
            self.jump_power -= 5
        elif self.jump_power <= 10:
            self.is_jump = False
            self.jump_power = 25

    def move_right(self):
        self.direction = "right"
        self.rect.x += self.speed
        self.update_right()

    def move_left(self):
        self.direction = "left"
        self.rect.x -= self.speed
        self.update_left()


class Playerinventary(pygame.sprite.Sprite):
    """Hero inventory sprite class"""

    def __init__(self, image, pos_x, pos_y, inventory_group, f=0):
        super().__init__(inventory_group)
        self.image = pygame.transform.scale(image, (30, 30))
        if f:
            self.rect = self.image.get_rect().move(pos_x, pos_y)
        else:
            self.rect = self.image.get_rect().move(35 * pos_x, pos_y + 5)


class Sword(pygame.sprite.Sprite):
    """Hero sword class"""

    def __init__(self, image, pos_x, pos_y, sword_group):
        super().__init__(sword_group)
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Health(pygame.sprite.Sprite):
    """Player health class"""

    def __init__(self,pos_x, pos_y, health_group, f=False):
        super().__init__(health_group)
        if f:
            self.image = pygame.transform.scale(tile_images["heart"], (30, 30))
        else:
            self.image = pygame.transform.scale(tile_images["full_heart"], (30, 30))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
