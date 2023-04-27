import pygame
from Images import tile_images


class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, enemy_group):
        super().__init__(enemy_group)
        self.gravity = 3
        self.speed_gravity = 1
        self.health = 100
        self.current_item_index = 0
        self.jump_power = 25
        self.is_jump = False
        self.speed = 3
        self.frames_right = [pygame.image.load("data/Enemy/zombie_right_1.png"),
                             pygame.image.load("data/Enemy/zombie_right_2.png"),
                             pygame.image.load("data/Enemy/zombie_right_3.png")]
        self.frames_left = [pygame.image.load("data/Enemy/zombie_left_1.png"),
                            pygame.image.load("data/Enemy/zombie_left_2.png"),
                            pygame.image.load("data/Enemy/zombie_left_3.png")]
        for img in range(3):
            self.frames_left[img] = pygame.transform.scale(self.frames_left[img], (25, 45))
            self.frames_right[img] = pygame.transform.scale(self.frames_right[img], (25, 45))
        self.image = self.frames_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = "right"

    def get_down(self):
        self.rect.y += self.gravity
        if self.gravity < 15:
            self.gravity += self.speed_gravity
            self.speed_gravity += 1

    def update_right(self):
        self.current_item_index += 1
        self.current_item_index %= 3
        self.image = self.frames_right[self.current_item_index]

    def update_left(self):
        self.current_item_index += 1
        self.current_item_index %= 3
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
