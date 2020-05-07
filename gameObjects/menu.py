import pygame
from gameObjects.button import Button


class Menu:
    def __init__(self, screen, window_width, window_height, editor=None):
        if editor is None:
            self.screen = screen
            self.window_width = window_width
            self.window_height = window_height
            self.background = pygame.image.load("resources/images/menu_background.jpg")
            self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))
            self.title = pygame.image.load("resources/images/title.png")
            self.buttons = {}
            pygame.mixer.music.load('resources/sounds/opening.mp3')
            pygame.mixer.music.play(-1)
        else:
            self.screen = screen
            self.window_width = window_width
            self.window_height = window_height

    def prepare_menu(self):
        play_button = Button(self.window_width, self.title.get_height(), "Play")
        map_editor_button = Button(self.window_width, self.title.get_height()
                                   + play_button.button_height, "Map Editor")
        self.buttons["play"] = play_button
        self.buttons["map editor"] = map_editor_button

    def draw(self):
        self.prepare_menu()
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, ((self.window_width - self.title.get_width()) // 2, self.title.get_height() // 2))
        for button_label in self.buttons:
            button = self.buttons.get(button_label)
            button.draw(self.screen)
