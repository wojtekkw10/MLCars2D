import pygame


class KeyboardEventHandler:
    KEY_PRESSED = "DOWN"
    KEY_NOTPRESSED = "UP"

    def __init__(self):
        self.keys = {}
        self.line1 = []
        self.line2 = []
        self.is_first_line = True
        self.mouse_click = None

    def reset(self):
        self.unicode_buffor = None
        self.mouse_click = None

    def process(self, event):

        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = KeyboardEventHandler.KEY_PRESSED
            self.unicode_buffor = event.unicode
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = KeyboardEventHandler.KEY_NOTPRESSED
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_click = pygame.mouse.get_pos()
            if event.button == 1:
                self.line1.append(pygame.mouse.get_pos())
            elif event.button == 3:
                self.line2.append(pygame.mouse.get_pos())

    def isPressed(self, key):
        try:
            if self.keys[key] == KeyboardEventHandler.KEY_PRESSED:
                return True
            else:
                return False
        except KeyError:  # No key defined
            return False
