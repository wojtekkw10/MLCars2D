import sys
import pygame
from handlers.keyboardEventHandler import KeyboardEventHandler
from game_objects_manager import GameObjectsManager


class ScreenManager:
    def __init__(self):
        super().__init__()
        self.size = self.window_width, self.window_height = 1200, 600

    def display(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)

        game_objects_manager = GameObjectsManager(self.window_width, self.window_height, screen)
        game_objects_manager.display_menu()
        game_objects_manager.prepare_track()

        keyboardEvents = KeyboardEventHandler()

        clock = pygame.time.Clock()
        fps = 200

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pass
                keyboardEvents.process(event)
                game_objects_manager.check_pressed_buttons(event)

            game_objects_manager.perform_action(keyboardEvents)

            pygame.display.flip()
            clock.tick(fps)
