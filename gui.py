import pygame


class GUI:
    def __init__(self, screen, window_width, window_height):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height
        self.background = pygame.image.load("resources/images/menu_background.jpg")
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))
        self.title = pygame.image.load("resources/images/title.png")
        pygame.mixer.music.load('resources/sounds/opening.mp3')
        pygame.mixer.music.play(-1)
