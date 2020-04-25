import sys
import pygame

from handlers.keyboardEventHandler import KeyboardEventHandler
from gameObjects.car import Car


# def pixel(surface, color, pos):
#    surface.fill(COLOR, (pos, (1, 1))


if __name__ == '__main__':
    pygame.init()

    size = width, height = 320, 240
    speed = [2, 2]
    white = 255, 255, 255
    car = Car(50, 50)

    screen = pygame.display.set_mode(size)
    keyboardEvents = KeyboardEventHandler()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            keyboardEvents.process(event)

        car.handle_keyboard(keyboardEvents)
        car.update()
        screen.fill(white)
        car.draw(screen)

        pygame.display.flip()
