import pygame, os, sys, time

from Player import Player, Playerinventary, Sword, Health
from Camera import Camera
from Map import Map, Tile
from Images import tile_images, load_image
from Enemy import Zombie

all_sprites: object = pygame.sprite.Group()
player_group: object = pygame.sprite.Group()
walls_group: object = pygame.sprite.Group()
tiles_group: object = pygame.sprite.Group()


class Game:
    def __init__(self) -> None:
        self.FPS: int = 19
        self.clock: object = pygame.time.Clock()
        self.GRAVITY: int = 5
        background_image_filename: str = 'data/Map/sheet.png'
        self.SCREEN_SIZE: tuple = (1024, 760)
        self.screen: object = pygame.display.set_mode(self.SCREEN_SIZE)
        self.background: object = pygame.image.load(background_image_filename).convert()
        self.map: Map = None
        self.player: Player = None

    def play(self) -> None:
        pygame.init()
        self.start_screen()

    def make_button(self, text: str, size: tuple, position: tuple, color: tuple) -> dict:
        """This function creates a button with the specified text, size, position and color."""
        font: object = pygame.font.SysFont('Arial', size)
        text_surf: object = font.render(text, True, color)
        text_rect: object = text_surf.get_rect(center=position)
        button_surf: object = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
        button_surf.fill((0, 0, 0, 0))
        button_surf.blit(text_surf, (10, 5))
        button_rect: object = button_surf.get_rect(center=position)
        return {'surface': button_surf, 'text_rect': text_rect, 'rect': button_rect}

    def start_screen(self) -> None:
        """This function is responsible for the start screen and for the selection of maps."""
        pygame.mixer.music.load('source/music.mp3')
        pygame.mixer.music.play()
        back_ground: object = load_image("data/Map/Startscreen.jpg", True)
        button_size: tuple = (200, 50)
        button_color: tuple = (250, 250, 250)
        button_hover_color: tuple = (117, 250, 97)
        map1_pos: tuple = (self.SCREEN_SIZE[0] / 2 - button_size[0] / 2 + 100, 660)
        map2_pos: tuple = (self.SCREEN_SIZE[0] / 2 - button_size[0] / 2 + 100, 720)
        exit_pos: tuple = (self.SCREEN_SIZE[0] - 20, 10)
        map1_button: object = self.make_button("Выбрать карту 1", 40, map1_pos, button_color)
        map2_button: object = self.make_button("Выбрать карту 2", 40, map2_pos, button_color)
        exit_button: object = self.make_button("X", 40, exit_pos, button_color)

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

            mouse_pos: object = pygame.mouse.get_pos()
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

    def fisrt_map_creation(self) -> None:
        for y in range(len(self.map.map)):
            for x in range(len(self.map.map[y])):
                if self.map.map[y][x] in tile_images.keys():
                    Tile(self.map.map[y][x], x, y, x, y, tiles_group, all_sprites)

    def Event_handler(self, key_down_flag, is_sword, sword_time, is_boost, boost_time, key_type):
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
                        if ((sprite.rect.x - self.player.rect.x) ** 2 +
                            (sprite.rect.y - self.player.rect.y) ** 2) ** 0.5 < 200:
                            flag = True
                            if sprite.type == "!":
                                is_boost = True
                                boost_time = 1000
                            else:
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
                        if ((sprite.rect.x - self.player.rect.x) ** 2 +
                            (sprite.rect.y - self.player.rect.y) ** 2) ** 0.5 < 200:
                            if sprite.rect.collidepoint(first_var):
                                Tile(list(self.player.inventory.keys())[self.player.inventory_index],
                                     sprite.rect.x + 25, sprite.rect.y, sprite.pos_x + 1, sprite.pos_y, tiles_group,
                                     all_sprites, 1)
                                self.player.inventory[
                                    list(self.player.inventory.keys())[self.player.inventory_index]] -= 1
                                if self.player.inventory[
                                    list(self.player.inventory.keys())[self.player.inventory_index]] == 0:
                                    del self.player.inventory[
                                        list(self.player.inventory.keys())[self.player.inventory_index]]
                                    self.player.inventory_index = 0
                                break
                            if sprite.rect.collidepoint(second_var):
                                Tile(list(self.player.inventory.keys())[self.player.inventory_index],
                                     sprite.rect.x - 25, sprite.rect.y, sprite.pos_x - 1, sprite.pos_y, tiles_group,
                                     all_sprites, 1)
                                self.player.inventory[
                                    list(self.player.inventory.keys())[self.player.inventory_index]] -= 1
                                if self.player.inventory[
                                    list(self.player.inventory.keys())[self.player.inventory_index]] == 0:
                                    del self.player.inventory[
                                        list(self.player.inventory.keys())[self.player.inventory_index]]
                                    self.player.inventory_index = 0

                                break
                            if sprite.rect.collidepoint(third_var):
                                Tile(list(self.player.inventory.keys())[self.player.inventory_index],
                                     sprite.rect.x, sprite.rect.y + 25, sprite.pos_x, sprite.pos_y + 1, tiles_group,
                                     all_sprites, 1)
                                self.player.inventory[
                                    list(self.player.inventory.keys())[self.player.inventory_index]] -= 1
                                if self.player.inventory[
                                    list(self.player.inventory.keys())[self.player.inventory_index]] == 0:
                                    del self.player.inventory[
                                        list(self.player.inventory.keys())[self.player.inventory_index]]
                                    self.player.inventory_index = 0

                                break
                            if sprite.rect.collidepoint(fourth_var):
                                Tile(list(self.player.inventory.keys())[self.player.inventory_index],
                                     sprite.rect.x, sprite.rect.y - 25, sprite.pos_x - 1, sprite.pos_y, tiles_group,
                                     all_sprites, 1)
                                self.player.inventory[
                                    list(self.player.inventory.keys())[self.player.inventory_index]] -= 1
                                if self.player.inventory[
                                    list(self.player.inventory.keys())[self.player.inventory_index]] == 0:
                                    del self.player.inventory[
                                        list(self.player.inventory.keys())[self.player.inventory_index]]
                                    self.player.inventory_index = 0

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
        # print(key_down_flag, is_sword, sword_time, is_boost, boost_time, 231)
        return key_down_flag, is_sword, sword_time, is_boost, boost_time, key_type

    def JumpAndGravity(self):
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

    def ZombieAndPlayerInteractino(self, zombie, enemy_group, sword_group):
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
            zombie.health -= self.player.damage
            if zombie.health <= 0:
                zombie = None
                enemy_group = pygame.sprite.Group()
            else:
                for i in range(5):
                    if zombie.rect.x < self.player.rect.x:
                        zombie.move_left()
                        if pygame.sprite.spritecollideany(zombie, tiles_group):
                            zombie.rect.x += zombie.speed
                    else:
                        zombie.move_right()
                        if pygame.sprite.spritecollideany(zombie, tiles_group):
                            zombie.rect.x -= zombie.speed
        return zombie, enemy_group, sword_group

    def game_loop(self) -> None:
        back_ground_day: pygame.Surface = load_image("data/Map/sheet.png", True)
        back_ground_night: pygame.Surface = load_image("data/Map/night.png", True)
        left_sword: pygame.Surface = load_image("data/Player/left_sword.png")
        right_sword: pygame.Surface = load_image("data/Player/sword.png")
        self.screen.blit(back_ground_day, (0, 0))
        self.player = Player(1000, 100, player_group, all_sprites)
        self.fisrt_map_creation()
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        sword_time: int = 0
        zombie_time: int = 0
        boost_time: int = 0
        is_boost: bool = False
        is_zombie: bool = False
        is_sword: bool = False
        zombie: Zombie = None
        clock: object = pygame.time.Clock()
        time: int = 28800
        key_down_flag: bool = False
        key_type: object = None
        camera: Camera = Camera()
        enemy_group: object = pygame.sprite.Group()
        while True:
            sword_group: object = pygame.sprite.Group()
            inventory_group: object = pygame.sprite.Group()
            health_group: object = pygame.sprite.Group()

            time += 10
            time %= 86400
            clock.tick(self.FPS)

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

            key_down_flag, is_sword, sword_time, is_boost, boost_time, key_type = \
                self.Event_handler(key_down_flag, is_sword, sword_time, is_boost, boost_time, key_type)

            self.JumpAndGravity()

            if is_boost:
                boost_time -= 10
                self.player.damage = 100
                if boost_time <= 0:
                    is_boost = False
                    self.player.damage = 10

            if is_sword:
                if self.player.direction == "right":
                    sword = Sword(right_sword, self.player.rect.x + 18, self.player.rect.y, sword_group)
                else:
                    sword = Sword(left_sword, self.player.rect.x - 28, self.player.rect.y, sword_group)

            if sword_time > 0:
                sword_time -= 20
                if sword_time <= 0:
                    sword_time = 0
                    is_sword = False
                    sword = None

            if zombie is not None:
                zombie, enemy_group, sword_group = self.ZombieAndPlayerInteractino(zombie, enemy_group, sword_group)
                if zombie is None:
                    is_zombie = False

            if time <= 18000 or time >= 72000:
                self.screen.blit(back_ground_night, (0, 0))
            else:
                self.screen.blit(back_ground_day, (0, 0))

            count_items_sprites = []
            count_item = 0
            for item in self.player.inventory:
                player_item = Playerinventary(tile_images[item], count_item, 0, inventory_group)
                count_items_sprites.append(
                    self.make_button(f"{self.player.inventory[list(self.player.inventory.keys())[count_item]]}", 20,
                                     (count_item * 35, 50),
                                     (117, 250, 141)))
                count_item += 1

            for i in range(10):
                if i * 10 < self.player.health:
                    heart = Health(self.SCREEN_SIZE[0] - 350 + 35 * i, 5, health_group, False)
                else:
                    heart = Health(self.SCREEN_SIZE[0] - 350 + 35 * i, 5, health_group, True)

            time_sprite = self.make_button(f"Time:{time // 60 // 60}h{(time % 3600) // 60}min", 20,
                                           (self.SCREEN_SIZE[0] - 70, 50),
                                           (117, 250, 141))

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
            health_group.draw(self.screen)
            for item_count in count_items_sprites:
                self.screen.blit(item_count["surface"], item_count["text_rect"])
            self.screen.blit(time_sprite["surface"], time_sprite["text_rect"])

            pygame.display.flip()
