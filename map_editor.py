import pygame
import files_ops


class MapEditor:
    def __init__(self, screen):
        self.screen = screen
        self.line_color = (148, 181, 51)
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
        if len(keyboard_events.start_positions) > 1 and len(keyboard_events.end_positions) > 1:
            for i in range(1, len(keyboard_events.start_positions)):
                pygame.draw.line(self.screen, self.line_color, keyboard_events.start_positions[i],
                                 keyboard_events.end_positions[i], 5)

    def handle_keyboard(self, keyboardEvents):
        if keyboardEvents.isPressed(mapped_key('s')):
            files_ops.save_map(keyboardEvents.start_positions, keyboardEvents.end_positions)
        if keyboardEvents.isPressed(mapped_key('l')):
            list = files_ops.load_map()
            keyboardEvents.start_positions = list[:len(list) // 2]
            keyboardEvents.end_positions = list[len(list) // 2:]
        if keyboardEvents.isPressed(mapped_key('b')):
            return True


def mapped_key(key):
    return {
        's': pygame.K_s,
        'l': pygame.K_l,
        'b': pygame.K_b
    }.get(key)


