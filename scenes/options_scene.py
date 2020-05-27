class OptionsScene:
    def update(self):


    def draw(self, screen):
        background_color = (186, 193, 204)
        screen.fill(background_color)
        # do some action hehe
        # self.track.initialize_points(False) - loads map from editor instead of default

        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render("If you want go go back, remember we never gonna give up and press 'b'"
                           , True, (255, 255, 255))
        textRect = text.get_rect()
        screen.blit(text, textRect)