import sys
import pygame

if __name__ == '__main__':
    pygame.init()

    size = width, height = 320, 240
    speed = [2, 2]
    white = 255, 255, 255

    screen = pygame.display.set_mode(size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(white)
        pygame.display.flip()
