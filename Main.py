import sys
import pygame
import math

from handlers.keyboardEventHandler import KeyboardEventHandler
from gameObjects.car import Car
from gameObjects.track import Track

# def pixel(surface, color, pos):
#    surface.fill(COLOR, (pos, (1, 1))


if __name__ == '__main__':

    pygame.init()

    fps = 200
    clock = pygame.time.Clock()

    size = width, height = 1200, 600
    speed = [2, 2]
    white = 255, 255, 255
    grey = (56, 59, 56)

    screen = pygame.display.set_mode(size)
    keyboardEvents = KeyboardEventHandler()

    track = Track(screen)
    car = Car(50, 60, screen)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            keyboardEvents.process(event)

        car.handle_keyboard(keyboardEvents)
        car.update()

        screen.fill(grey)


        car_position_x, car_position_y = int(car.position_x), int(car.position_y)
        if car.detect_collision(track.grid):
            print("Collision")

        track.draw_track()
        car.draw(screen)

        pygame.display.flip()
        clock.tick(fps)