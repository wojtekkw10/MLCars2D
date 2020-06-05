import pygame


class Button:
    BG_COLOR = 255, 255, 255
    ACTIVE_COLOR = 211, 211, 211

    def __init__(self, x, y, label_text):
        self.btn_text = label_text
        self.button_width = 250
        self.button_height = 65
        self.button_bg_color = 211, 211, 211
        self.x = (x - self.button_width) / 2
        self.y = y * 2
        self.is_button_pressed = False

    def draw(self, screen):
        self.draw_btn_rect(screen)
        self.draw_btn_text(screen)

    def draw_btn_rect(self, screen):
        button_rect = (self.x, self.y, self.button_width, self.button_height)
        pygame.draw.rect(screen, self.button_bg_color, button_rect, 0)

    def draw_btn_text(self, screen):
        if self.btn_text != '':
            font = pygame.font.SysFont('comicsans', 60)
            font_color = (0, 0, 0)
            antialias = 1
            text = font.render(self.btn_text, antialias, font_color)
            text_destination = (self.x + (self.button_width / 2 - text.get_width() / 2),
                                    self.y + (self.button_height / 2 - text.get_height() / 2))
            screen.blit(text, text_destination)

    def check_is_button_pressed(self, event, screen):
        if self.is_mouse_over(pygame.mouse.get_pos()):
            self.button_bg_color = Button.ACTIVE_COLOR
            self.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_over(pygame.mouse.get_pos()):
                self.is_button_pressed = True
        else:
            self.button_bg_color = Button.BG_COLOR
            self.draw(screen)

    def is_mouse_over(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.button_width:
            if self.y < mouse_pos[1] < self.y + self.button_height:
                return True

        return False
