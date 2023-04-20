import pygame, os, sys, time

from Player import Player, Playerinventary, Sword
from Camera import Camera
from Map import Map, Tile
from Images import tile_images, load_image
from Enemy import Zombie

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


class Game:
    def __init__(self):
        self.FPS = 19
        self.map = 0
        self.clock = pygame.time.Clock()
        self.GRAVITY = 5
        background_image_filename = 'data/Map/sheet.png'
        self.SCREEN_SIZE = (1024, 760)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.background = pygame.image.load(background_image_filename).convert()
        self.map = None
        self.player = None

    def play(self):
        pygame.init()
        self.start_screen()

    def make_button(self, text: str, size: tuple, position: tuple, color: tuple):
        """This function creates a button with the specified text, size, position and color."""
        font = pygame.font.SysFont('Arial', size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=position)
        button_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
        button_surf.fill((0, 0, 0, 0))
        button_surf.blit(text_surf, (10, 5))
        button_rect = button_surf.get_rect(center=position)
        return {'surface': button_surf, 'text_rect': text_rect, 'rect': button_rect}

    def start_screen(self):
        """This function is responsible for the start screen and for the selection of maps."""
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play()
        back_ground = load_image("data/Map/Startscreen.jpg", True)
        button_size = (200, 50)
        button_color = (250, 250, 250)
        button_hover_color = (117, 250, 97)
        map1_pos = (self.SCREEN_SIZE[0] / 2 - button_size[0] / 2 + 100, 660)
        map2_pos = (self.SCREEN_SIZE[0] / 2 - button_size[0] / 2 + 100, 720)
        exit_pos = (self.SCREEN_SIZE[0] - 20, 10)
        map1_button = self.make_button("Выбрать карту 1", 40, map1_pos, button_color)
        map2_button = self.make_button("Выбрать карту 2", 40, map2_pos, button_color)
        exit_button = self.make_button("X", 40, exit_pos, button_color)

        while True:
            self.screen.blit(back_ground, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if map1_button['rect'].collidepoint(event.pos):
                        self.map = Map("data/Map/first_map.txt")
                        self.game_loop()
                        return
                    elif map2_button['rect'].collidepoint(event.pos):
                        self.map = Map("data/Map/second_map.txt")
                        self.game_loop()
                        return
                    elif exit_button['rect'].collidepoint(event.pos):
                        pygame.quit()
                        return

            mouse_pos = pygame.mouse.get_pos()
            if map1_button['rect'].collidepoint(mouse_pos):
                map1_button = self.make_button("Выбрать карту 1", 40, map1_pos, button_hover_color)
            else:
                map1_button = self.make_button("Выбрать карту 1", 40, map1_pos, button_color)

            if map2_button['rect'].collidepoint(mouse_pos):
                map2_button = self.make_button("Выбрать карту 2", 40, map2_pos, button_hover_color)
            else:
                map2_button = self.make_button("Выбрать карту 2", 40, map2_pos, button_color)

            if exit_button['rect'].collidepoint(mouse_pos):
                exit_button = self.make_button("X", 40, exit_pos, button_hover_color)
            else:
                exit_button = self.make_button("X", 40, exit_pos, button_color)

            self.screen.blit(back_ground, (0, 0))
            self.screen.blit(map1_button['surface'], map1_button['text_rect'])
            self.screen.blit(map2_button['surface'], map2_button['text_rect'])
            self.screen.blit(exit_button['surface'], exit_button['text_rect'])
            pygame.display.flip()

    def update_frames(self):
        player_info = [self.player.rect.x, self.player.rect.y,
                       self.player.cur_frame_left, self.player.cur_frame_right]

    def fisrt_map_creation(self):
        for y in range(len(self.map.map)):
            for x in range(len(self.map.map[y])):
                if self.map.map[y][x] in tile_images.keys():
                    Tile(self.map.map[y][x], x, y, x, y, tiles_group, all_sprites)

    def update_sprites(self):
        pass

    def game_loop(self):
        back_ground_day = load_image("data/Map/sheet.png", True)
        back_ground_night = load_image("data/Map/night.png", True)
        left_sword = load_image("data/Player/left_sword.png")
        right_sword = load_image("data/Player/sword.png")
        self.screen.blit(back_ground_day, (0, 0))
        self.player = Player(1000, 100, player_group, all_sprites)
        self.fisrt_map_creation()
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        sword_time = 0
        zombie_time = 0
        is_zombie = False
        is_sword = False
        zombie = None
        clock = pygame.time.Clock()
        time = 28800
        key_down_flag = False
        key_type = None
        camera = Camera()
        enemy_group = pygame.sprite.Group()
        while True:
            sword_group = pygame.sprite.Group()
            inventory_group = pygame.sprite.Group()
            time += 10
            zombie_time += 1
            zombie_time %= 1000
            if zombie_time == 900 and is_zombie == False:
                is_zombie = True
            if is_zombie and zombie is None:
                if time % 2 == 0:
                    zombie = Zombie(self.player.rect.x - 150, self.player.rect.y, enemy_group)
                else:
                    zombie = Zombie(self.player.rect.x + 150, self.player.rect.y, enemy_group)
                while pygame.sprite.spritecollideany(zombie, tiles_group):
                    zombie.rect.y -= 50
            time %= 86400
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    key_down_flag = True
                    key_type = event.key
                elif event.type == pygame.KEYUP:
                    key_down_flag = False
                    self.player.update()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player.inventory_index == 0:
                        sword_time = 100
                        is_sword = True
                    flag = False
                    for sprite in tiles_group:
                        if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                            # удаление спрайта из группы
                            flag = True
                            if sprite.type in self.player.inventory:
                                self.player.inventory[sprite.type] += 1
                            else:
                                self.player.inventory[sprite.type] = 1
                            tiles_group.remove(sprite)
                            all_sprites.remove(sprite)
                            break
                    if self.player.inventory_index != 0 and flag == False:
                        mouse_cords = list(pygame.mouse.get_pos())
                        first_var = mouse_cords.copy()
                        second_var = mouse_cords.copy()
                        third_var = mouse_cords.copy()
                        fourth_var = mouse_cords.copy()
                        first_var[0] -= 25
                        second_var[0] += 25
                        third_var[1] -= 25
                        fourth_var[1] += 25
                        for sprite in tiles_group:
                            if sprite.rect.collidepoint(first_var):
                                Tile(list(self.player.inventory.keys())[self.player.inventory_index],
                                     sprite.rect.x + 25, sprite.rect.y, sprite.pos_x + 1, sprite.pos_y, tiles_group,
                                     all_sprites, 1)
                                break
                            if sprite.rect.collidepoint(second_var):
                                Tile(list(self.player.inventory.keys())[self.player.inventory_index],
                                     sprite.rect.x - 25, sprite.rect.y, sprite.pos_x - 1, sprite.pos_y, tiles_group,
                                     all_sprites, 1)
                                break
                            if sprite.rect.collidepoint(third_var):
                                Tile(list(self.player.inventory.keys())[self.player.inventory_index],
                                     sprite.rect.x, sprite.rect.y + 25, sprite.pos_x, sprite.pos_y + 1, tiles_group,
                                     all_sprites, 1)
                                break
                            if sprite.rect.collidepoint(fourth_var):
                                Tile(list(self.player.inventory.keys())[self.player.inventory_index],
                                     sprite.rect.x, sprite.rect.y - 25, sprite.pos_x - 1, sprite.pos_y, tiles_group,
                                     all_sprites, 1)
                                break
                if key_down_flag:
                    if key_type == pygame.K_d:
                        self.player.move_right()
                        if pygame.sprite.spritecollideany(self.player, tiles_group):
                            self.player.rect.x -= self.player.speed
                    if key_type == pygame.K_a:
                        self.player.move_left()
                        if pygame.sprite.spritecollideany(self.player, tiles_group):
                            self.player.rect.x += self.player.speed
                    elif key_type == pygame.K_SPACE:
                        self.player.rect.y += 10
                        if pygame.sprite.spritecollideany(self.player, tiles_group):
                            self.player.is_jump = True
                        self.player.rect.y -= 10
                    if key_type == pygame.K_1 or key_type == pygame.K_2 or key_type == pygame.K_3 or \
                            key_type == pygame.K_4 or key_type == pygame.K_5 or key_type == pygame.K_6 or \
                            key_type == pygame.K_7 or key_type == pygame.K_8:
                        if len(list(self.player.inventory.keys())) > key_type - 49:
                            self.player.inventory_index = key_type - 49
            if not pygame.sprite.spritecollideany(self.player, tiles_group):
                prev_y = self.player.rect.y
                self.player.get_down()
                if pygame.sprite.spritecollideany(self.player, tiles_group):
                    self.player.rect.y = prev_y
                    self.player.gravity = 3
                    self.player.speed_gravity = 1
            else:
                self.player.gravity = 3
                self.player.speed_gravity = 1
            if self.player.is_jump:
                prev_y = self.player.rect.y
                self.player.jump()
                if pygame.sprite.spritecollideany(self.player, tiles_group):
                    self.player.rect.y = prev_y
                    self.player.is_jump = False
            if is_sword:
                if self.player.direction == "right":
                    sword = Sword(right_sword, self.player.rect.x + 18, self.player.rect.y, sword_group)
                else:
                    sword = Sword(left_sword, self.player.rect.x - 28, self.player.rect.y, sword_group)
            if sword_time > 0:
                sword_time -= 20
                # sword.image = pygame.transform.rotate(sword.image, 10)
                if sword_time <= 0:
                    sword_time = 0
                    is_sword = False
                    sword = None
            if zombie is not None:
                if pygame.sprite.spritecollideany(self.player, enemy_group):
                    self.player.health -= 10
                    for i in range(5):
                        if zombie.rect.x > self.player.rect.x:
                            self.player.move_left()
                            if pygame.sprite.spritecollideany(self.player, tiles_group):
                                self.player.rect.x += self.player.speed
                        else:
                            self.player.move_right()
                            if pygame.sprite.spritecollideany(self.player, tiles_group):
                                self.player.rect.x -= self.player.speed
                else:
                    if zombie.rect.x > self.player.rect.x:
                        zombie.move_left()
                        if pygame.sprite.spritecollideany(zombie, tiles_group):
                            zombie.rect.x += zombie.speed
                    else:
                        zombie.move_right()
                        if pygame.sprite.spritecollideany(zombie, tiles_group):
                            zombie.rect.x -= zombie.speed
                if not pygame.sprite.spritecollideany(zombie, tiles_group):
                    prev_y = zombie.rect.y
                    zombie.get_down()
                    if pygame.sprite.spritecollideany(zombie, tiles_group):
                        zombie.rect.y = prev_y
                        zombie.gravity = 3
                        zombie.speed_gravity = 1
                else:
                    zombie.gravity = 3
                    zombie.speed_gravity = 1
                if zombie.rect.y > self.player.rect.y:
                    zombie.rect.y += 10
                    if pygame.sprite.spritecollideany(zombie, tiles_group):
                        zombie.rect.y -= 10
                        zombie.is_jump = True
                if zombie.is_jump:
                    prev_y = zombie.rect.y
                    zombie.jump()
                    if pygame.sprite.spritecollideany(zombie, tiles_group):
                        zombie.rect.y = prev_y
                        zombie.is_jump = False
                if pygame.sprite.spritecollideany(zombie, sword_group):
                    zombie.health -= 34
                    if zombie.health <= 0:
                        zombie = None
                        is_zombie = False
                        enemy_group = pygame.sprite.Group()
            if time <= 18000 or time >= 72000:
                self.screen.blit(back_ground_night, (0, 0))
            else:
                self.screen.blit(back_ground_day, (0, 0))

            count_item = 0
            for item in self.player.inventory:
                player_item = Playerinventary(tile_images[item], count_item, count_item, inventory_group)
                count_item += 1

            health = self.make_button(f"health: {self.player.health}", 20, (self.SCREEN_SIZE[0] - 70, 10),
                                      (117, 250, 141))
            time_sprite = self.make_button(f"Time:{time // 60 // 60}h{(time % 3600) // 60}min", 20,
                                           (self.SCREEN_SIZE[0] - 70, 30),
                                           (117, 250, 141))
            self.screen.blit(health["surface"], health["text_rect"])
            self.screen.blit(time_sprite["surface"], time_sprite["text_rect"])

            if self.player.health == 0:
                self.start_screen()

            camera.update(self.player)
            for sprite in tiles_group:
                camera.apply(sprite)
            for sprite in player_group:
                camera.apply(sprite)
            for sprite in enemy_group:
                camera.apply(sprite)
            for sprite in sword_group:
                camera.apply(sprite)

            all_sprites.draw(self.screen)
            sword_group.draw(self.screen)
            inventory_group.draw(self.screen)
            enemy_group.draw(self.screen)
            pygame.display.flip()
