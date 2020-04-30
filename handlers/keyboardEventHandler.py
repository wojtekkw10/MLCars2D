import pygame


class KeyboardEventHandler:
    KEY_PRESSED = "DOWN"
    KEY_NOTPRESSED = "UP"

    def __init__(self):
        self.keys = {}

    def process(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = KeyboardEventHandler.KEY_PRESSED
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = KeyboardEventHandler.KEY_NOTPRESSED

    def isPressed(self, key):
        try:
            if self.keys[key] == KeyboardEventHandler.KEY_PRESSED:
                return True
            else:
                return False
        except KeyError:  # No key defined
            return False
