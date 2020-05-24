import pygame


class KeyboardEventHandler:
    KEY_PRESSED = "DOWN"
    KEY_NOTPRESSED = "UP"

    def __init__(self):
        self.keys = {}
        self.start_positions = []
        self.end_positions = []
        self.is_drawing_line = False

    def process(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = KeyboardEventHandler.KEY_PRESSED
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = KeyboardEventHandler.KEY_NOTPRESSED
        elif event.type == pygame.MOUSEBUTTONUP and self.is_drawing_line:
            self.end_positions.append(pygame.mouse.get_pos())
            self.is_drawing_line = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.start_positions.append(pygame.mouse.get_pos())
            self.is_drawing_line = True

    def isPressed(self, key):
        try:
            if self.keys[key] == KeyboardEventHandler.KEY_PRESSED:
                return True
            else:
                return False
        except KeyError:  # No key defined
            return False

