import sys
import pygame
from gameObjects.Button import Button

if __name__ == '__main__':

    pygame.init()
    size = window_width, window_height = 1200, 600

    screen = pygame.display.set_mode(size)
    background = pygame.image.load("resources/images/menu_background.jpg")
    background = pygame.transform.scale(background, (window_width, window_height))
    title = pygame.image.load("resources/images/title.png")
    pygame.mixer.music.load('resources/sounds/opening.mp3')
    pygame.mixer.music.play(-1)
    buttons_bg = 211, 211, 211
    buttons_width, buttons_height = 200, 65

    play_button = Button(buttons_bg, (window_width - buttons_width) / 2, title.get_height() * 2,
                         buttons_width, buttons_height, "Play")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(title, ((window_width - title.get_width()) / 2, title.get_height() / 2))
        play_button.draw(screen)

        if play_button.is_over(pygame.mouse.get_pos()):
            play_button.color = 255, 255, 255
        else:
            play_button.color = buttons_bg

        pygame.display.flip()
