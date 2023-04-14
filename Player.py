import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.inventory = ["ball"] + [None] * 9
        self.current_item_index = 0
        self.jump_power = 10
        self.speed = 5
        self.frames_right = [pygame.image.load("data/Player/player.png"),
                             pygame.image.load("data/Player/right2.png"),
                             pygame.image.load("data/Player/right3.png"),
                             pygame.image.load("data/Player/right4.png")]
        self.frames_left = [pygame.image.load("data/Player/sprite1.png"),
                             pygame.image.load("data/Player/sprite2.png"),
                             pygame.image.load("data/Player/sprite3.png"),
                             pygame.image.load("data/Player/sprite4.png")]
        self.image = self.frames_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = "right"
        self.sword_image = pygame.image.load("data/Player/sword.png")
        self.sword_rotated_image = self.sword_image
        self.sword_angle = 0
        self.sword_is_rotating = False
        self.sword_rotation_speed = 10

    def update_right(self):
        self.current_item_index = 0
        self.image = self.frames_right[(self.frames_right.index(self.image) + 1) % 4]

    def update_left(self):
        self.current_item_index = 0
        self.image = self.frames_left[(self.frames_left.index(self.image) + 1) % 4]

    def jump(self):
        if self.rect.bottom == 600:
            self.rect.y -= 1
            self.rect.y -= self.jump_power
            self.jump_power -= 1
            if self.jump_power == 0:
                self.jump_power = 10

    def move_right(self):
        self.direction = "right"
        self.rect.x += self.speed
        self.update_right()

    def move_left(self):
        self.direction = "left"
        self.rect.x -= self.speed
        self.update_left()

    def hit_with_ball(self):
        if self.current_item_index == 0:
            if self.direction == "right":
                self.rotate_sword(-90)
            else:
                self.rotate_sword(90)

    def change_item(self, index):
        self.current_item_index = index
        if self.inventory[index] == "ball":
            self.image = self.frames_right[0]
        else:
            self.rotate_sword(0)

    def rotate_sword(self, angle):
        self.sword_is_rotating = True
        self.sword_angle = angle

    def update_sword(self):
        if self.sword_is_rotating:
            self.sword_rotated_image = pygame.transform.rotate
