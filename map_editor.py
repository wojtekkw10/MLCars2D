import pygame
import files_ops


class MapEditor:
    def __init__(self, screen):
        self.screen = screen
        self.line1_color = (148, 181, 51)
        self.line2_color = (55, 16, 21)
        self.first_attempt = True
        self.clean = True

    def draw_editor(self):
        if self.clean:
            self.screen.fill((56, 59, 56))
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render("If you want to save your map, press 's'. If you want load saved map, press 'l'. "
                               "If you want go go back, remember we never gonna give up and press 'b"
                               , True, (255, 255, 255))
            textRect = text.get_rect()
            self.screen.blit(text, textRect)
            self.clean = False

    def draw_map(self, keyboard_events):

        print(keyboard_events.line1)

        if keyboard_events.is_drawing_line:
            keyboard_events.line1 = []
            keyboard_events.is_drawing_line = False

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
            keyboardEvents.line2 = list[half+1:]
        if keyboardEvents.isPressed(mapped_key('b')):
            return True


def mapped_key(key):
    return {
        's': pygame.K_s,
        'l': pygame.K_l,
        'b': pygame.K_b,
        'e': pygame.K_e
    }.get(key)
