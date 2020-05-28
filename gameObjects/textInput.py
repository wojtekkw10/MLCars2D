import pygame


class TextInput:
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    TEXT_MODE = "Text"
    NUMBER_MODE = "Number"

    def __init__(self, x, y, width, height, mode="Text"):
        self.input_box = pygame.Rect(
            x, y, width, height)
        self.text_buffor = ""
        self.color = TextInput.COLOR_INACTIVE
        self.input_active = False
        self.mode = mode

    def update(self, keyboard_events):
        if keyboard_events.mouse_click is not None:
            if self.input_box.collidepoint(keyboard_events.mouse_click):
                self.input_active = True
                self.color = TextInput.COLOR_ACTIVE
            else:
                self.input_active = False
                self.color = TextInput.COLOR_INACTIVE

        if self.input_active:
            if keyboard_events.isPressed(pygame.K_RETURN):
                self.text_buffor = ""
            elif keyboard_events.isPressed(pygame.K_BACKSPACE):
                self.text_buffor = self.text_buffor[:-1]
            elif keyboard_events.unicode_buffor != None:
                nums = [f"{i}" for i in range(10)]
                if self.mode == TextInput.NUMBER_MODE:
                    if keyboard_events.unicode_buffor in nums:
                        self.text_buffor += keyboard_events.unicode_buffor
                else:
                    self.text_buffor += keyboard_events.unicode_buffor

    def draw(self, screen, font):
        txt_surface = font.render(self.text_buffor, True, self.color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)
