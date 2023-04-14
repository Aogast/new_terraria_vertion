class Person(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames = player_image
        self.image = self.frames[0]
        self.cur_frame_right = 0
        self.number_bloc = 0
        self.cur_frame_left = 0




    def update_right(self):
        self.cur_frame_right = 1 + ((self.cur_frame_right + 1) % 5)
        self.image = self.frames[self.cur_frame_right]

    def update_left(self):
        self.cur_frame_left = 7 + ((self.cur_frame_left + 1) % 5)
        self.image = self.frames[self.cur_frame_left]

    def update(self):
        self.image = self.frames[0]

    def left_jump(self):
        pass

    def right_jump(self):
        pass

    def jump(self):
        pass
