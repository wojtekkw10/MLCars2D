import sys
import pygame
from handlers.keyboardEventHandler import KeyboardEventHandler
from game_objects_controller import GameObjectsController


class ScreenController:
    def __init__(self):
        super().__init__()
        self.size = self.window_width, self.window_height = 1200, 600

    def display(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)

        game_objects_controller = GameObjectsController(self.window_width, self.window_height, screen)
        game_objects_controller.display_menu()
        game_objects_controller.prepare_track()

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
                game_objects_controller.check_pressed_buttons(event)

            game_objects_controller.perform_action(keyboardEvents)

            pygame.display.flip()
            clock.tick(fps)
