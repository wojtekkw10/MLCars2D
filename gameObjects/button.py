import pygame


class Button:
    BG_COLOR = 211, 211, 211
    ACTIVE_COLOR = 0, 100, 100

    def __init__(self, x, y, label):
        self.label = label
        self.button_width = 200
        self.button_height = 65
        self.button_bg = 211, 211, 211
        self.x = (x - self.button_width) / 2
        self.y = y * 2
        self.is_button_pressed = False

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2,
                                               self.button_width + 4, self.button_height + 4), 0)

        pygame.draw.rect(screen, self.button_bg, (self.x, self.y,
                                                  self.button_width, self.button_height), 0)

        if self.label != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.label, 1, (0, 0, 0))
            screen.blit(text, (
                self.x + (self.button_width / 2 - text.get_width() / 2), self.y
                + (self.button_height / 2 - text.get_height() / 2)))

    def check_is_button_pressed(self, event, screen):
        if self.is_mouse_over(pygame.mouse.get_pos()):
            print("tak")
            self.button_bg = Button.ACTIVE_COLOR
            self.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_over(pygame.mouse.get_pos()):
                self.is_button_pressed = True
        else:
            self.button_bg = Button.BG_COLOR
            self.draw(screen)

    def is_mouse_over(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.button_width:
            if self.y < mouse_pos[1] < self.y + self.button_height:
                return True

        return False


