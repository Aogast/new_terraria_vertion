import pygame, os, sys

from Player import Player


class Game:
    def __init__(self):
        self.FPS = 60
        self.map = 0
        self.clock = pygame.time.Clock()
        self.GRAVITY = 5
        background_image_filename = 'data/Map/sheet.png'
        self.SCREEN_SIZE = (1024, 760)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.background = pygame.image.load(background_image_filename).convert()

    def play(self):
        pygame.init()
        self.start_screen()

    def load_image(self, name, colorkey=False):
        """This function allows you to load images from the data folder."""
        image = pygame.image.load(name)
        if colorkey:
            image = pygame.transform.scale(image, self.SCREEN_SIZE)
        image = image.convert_alpha()
        return image

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
        back_ground = self.load_image("data/Map/Startscreen.png", True)
        button_size = (200, 50)
        button_color = (250, 250, 250)
        button_hover_color = (0, 255, 100)
        map1_pos = (self.SCREEN_SIZE[0] / 2 - button_size[0] / 2 + 70, 630)
        map2_pos = (self.SCREEN_SIZE[0] / 2 - button_size[0] / 2 + 70, 700)
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
                    if map1_button['rect'].collidepoint(event.pos) or map2_button['rect'].collidepoint(event.pos):
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

    def game_loop(self):
        back_ground = self.load_image("data/Map/sheet.png", True)
        self.screen.blit(back_ground, (0, 0))
        player = Player(100, 100)
        self.screen.blit(player.image, (player.rect.x, player.rect.y))
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        player.move_right()
                        player.update_right()
                    if event.key == pygame.K_a:
                        player.move_left()
                        player.update_left()
            self.screen.blit(player.image, (player.rect.x, player.rect.y))
            pygame.display.flip()

