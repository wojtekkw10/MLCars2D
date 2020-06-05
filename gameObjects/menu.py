import pygame
from gameObjects.button import Button


class Menu:

    def __init__(self, screen, window_width, window_height):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height
        self.background = pygame.image.load("resources/images/menu_background.jpg")
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))
        self.title = pygame.image.load("resources/images/title.png")
        self.buttons = {}
        self.prepare_menu()
        # pygame.mixer.music.load('resources/sounds/opening.mp3')
        # pygame.mixer.music.play(-1)

    def prepare_menu(self):
        play_button = Button(self.window_width, self.title.get_height(), "Play")
        map_editor_button = Button(self.window_width, self.title.get_height()
                                   + play_button.button_height, "Map Editor")
        options_button = Button(self.window_width, self.title.get_height()
                                + play_button.button_height + map_editor_button.button_height
                                , "Options")

        self.buttons["play"] = play_button
        self.buttons["map editor"] = map_editor_button
        self.buttons["options"] = options_button

    def draw_main_menu(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, ((self.window_width - self.title.get_width()) // 2, self.title.get_height() // 2))
        for button_label in self.buttons:
            if button_label != "back":
                button = self.buttons.get(button_label)
                button.draw(self.screen)
