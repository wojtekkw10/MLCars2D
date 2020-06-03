import pygame
import files_ops
from gameObjects.button import Button


class MapEditor:
    def __init__(self, screen):
        self.screen = screen
        self.line1_color = (148, 181, 51)
        self.line2_color = (55, 16, 21)
        self.buttons = {}
        self.clean = True
        self.prepare_buttons()

    def draw_editor(self):
        if self.clean:
            self.screen.fill((56, 59, 56))
            self.draw_buttons(self.screen)
            self.clean = False

    def draw_map(self, keyboard_events):
        if keyboard_events.is_first_line:
            keyboard_events.line1 = []
            keyboard_events.is_first_line = False

        for i in range(0, len(keyboard_events.line1) - 1):
            pygame.draw.line(self.screen, self.line1_color, keyboard_events.line1[i],
                             keyboard_events.line1[i + 1], 5)
        for i in range(0, len(keyboard_events.line2) - 1):
            pygame.draw.line(self.screen, self.line2_color, keyboard_events.line2[i],
                             keyboard_events.line2[i + 1], 5)

    def handle_keyboard(self, keyboardEvents):
        if keyboardEvents.isPressed(mapped_key('e')):
            self.screen.fill((56, 59, 56))
            keyboardEvents.line1, keyboardEvents.line2 = [], []
        if keyboardEvents.isPressed(mapped_key('s')):
            files_ops.save_map(keyboardEvents.line1, keyboardEvents.line2)
        if keyboardEvents.isPressed(mapped_key('l')):
            list = files_ops.load_map()
            half = list.index((1000000, 1000000))
            keyboardEvents.line1 = list[:half]
            keyboardEvents.line2 = list[half + 1:]
        if keyboardEvents.isPressed(mapped_key('b')):
            return True

    def draw_buttons(self, screen):
        for button_label in self.buttons:
            button = self.buttons.get(button_label)
            button.draw(screen)

    def prepare_buttons(self):
        back_button = Button(2140, 265, "Back")
        self.buttons["back"] = back_button


def mapped_key(key):
    return {
        's': pygame.K_s,
        'l': pygame.K_l,
        'b': pygame.K_b,
        'e': pygame.K_e
    }.get(key)
