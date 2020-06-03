import pygame

from gameObjects.button import Button
from gameObjects.textInput import TextInput


class OptionsScene:

    def __init__(self, window_width, window_height):
        super().__init__()
        self.buttons = {}
        self.window_width = window_width
        self.window_height = window_height
        self.label_box = pygame.Rect(
            window_width / 2 - 70, window_height / 2 - 32, 140, 32)

        self.text_input = TextInput(
            window_width / 2 - 70, window_height / 2 - 16, 140, 32, mode=TextInput.NUMBER_MODE)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.prepare_buttons()

    def update(self, keyboard_events):
        self.text_input.update(keyboard_events)

    def get_cars_amount(self):
        return self.text_input.text_buffor

    def draw(self, screen):
        background_color = (186, 193, 204)
        screen.fill(background_color)
        self.text_input.draw(screen, self.font)
        self.draw_label(screen)
        self.draw_buttons(screen)

        self.clock.tick(30)

    def draw_label(self, screen):
        text = self.font.render(
            "Insert cars amount ...", True, (255, 255, 255))
        screen.blit(text, self.label_box)

    def draw_buttons(self, screen):
        for button_label in self.buttons:
            button = self.buttons.get(button_label)
            button.draw(screen)

    def prepare_buttons(self):
        back_button = Button(2140, 265, "Back")
        change_map_button = Button(2140, 225
                                   , "Load Track")
        self.buttons["back"] = back_button
        self.buttons["custom_map"] = change_map_button
