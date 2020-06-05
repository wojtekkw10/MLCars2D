import pygame
import files_ops
import constants
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
            self.draw_instructions()
            image = pygame.image.load('resources/images/car.png')
            self.screen.blit(image, constants.CAR_POSITION)
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
        if keyboardEvents.is_pressed(mapped_key('s')):
            files_ops.save_map(keyboardEvents.line1, keyboardEvents.line2)
        if keyboardEvents.is_pressed(mapped_key('l')):
            mapa = files_ops.load_map()
            half = mapa.index(constants.HALF)
            keyboardEvents.line1 = mapa[:half]
            keyboardEvents.line2 = mapa[half + 1:]

    def draw_buttons(self, screen):
        for button_label in self.buttons:
            button = self.buttons.get(button_label)
            button.draw(screen)

    def prepare_buttons(self):
        back_button = Button(2400, 265, "Back")
        erase_button = Button(2400, 240, "Erase")
        self.buttons["back"] = back_button
        self.buttons["erase"] = erase_button

        for button_label in self.buttons:
            button = self.buttons.get(button_label)
            button.button_width = 100
            button.button_height = 45
            button.font_size = constants.SMALL_FONT

    def draw_instructions(self):
        green = (0, 255, 0)
        font = pygame.font.Font('freesansbold.ttf', 10)
        text1 = font.render('Left Mouse Button - draw first line ', True, green)
        text2 = font.render('Right Mouse Button - draw second line', True, green)
        text3 = font.render('Press S for save map', True, green)
        text4 = font.render('Press L for load previous map', True, green)

        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect3 = text3.get_rect()
        textRect4 = text4.get_rect()

        textRect4.midleft = (constants.EDITOR_INSTRUCTIOS_X,
                             constants.EDITOR_INSTRUCTIOS_Y)
        textRect3.midleft = (constants.EDITOR_INSTRUCTIOS_X,
                             constants.EDITOR_INSTRUCTIOS_Y - 15)
        textRect2.midleft = (constants.EDITOR_INSTRUCTIOS_X,
                             constants.EDITOR_INSTRUCTIOS_Y - 30)
        textRect1.midleft = (constants.EDITOR_INSTRUCTIOS_X,
                             constants.EDITOR_INSTRUCTIOS_Y - 45)

        self.screen.blit(text1, textRect1)
        self.screen.blit(text2, textRect2)
        self.screen.blit(text3, textRect3)
        self.screen.blit(text4, textRect4)


def mapped_key(key):
    return {
        's': pygame.K_s,
        'l': pygame.K_l,
    }.get(key)
