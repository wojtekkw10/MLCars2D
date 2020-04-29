import sys
import pygame

if __name__ == '__main__':

    pygame.init()
    size = window_width, window_height = 720, 480

    screen = pygame.display.set_mode(size)
    background = pygame.image.load("resources/images/menu_background.jpg")
    title = pygame.image.load("resources/images/title.png")
    pygame.mixer.music.load('resources/sounds/opening.mp3')
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(title, (200, 25))
        pygame.display.flip()
