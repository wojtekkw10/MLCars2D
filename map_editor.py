import pygame


class MapEditor:
    def __init__(self, screen):
        self.screen = screen
        self.line_color = (148, 181, 51)
        self.clean = True

    def draw_editor(self):
        if self.clean:
            self.screen.fill((255, 255, 255))
            self.clean = False

    def draw_map(self, keyboard_events):
        if len(keyboard_events.start_positions) > 1 and len(keyboard_events.end_positions) > 1:
            for i in range(1, len(keyboard_events.start_positions)):
                pygame.draw.line(self.screen, self.line_color, keyboard_events.start_positions[i],
                                 keyboard_events.end_positions[i], 5)
