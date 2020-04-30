import sys
import pygame

from gameObjects.Button import Button
from gui import GUI

import math
from handlers.keyboardEventHandler import KeyboardEventHandler
from gameObjects.car import Car
from gameObjects.track import Track

# def pixel(surface, color, pos):
#    surface.fill(COLOR, (pos, (1, 1))


if __name__ == '__main__':

    pygame.init()
    size = window_width, window_height = 1200, 600
    screen = pygame.display.set_mode(size)

    gui = GUI(screen, window_width, window_height)
    play_button = Button(window_width, gui.title.get_height(), "Play")
    is_play_button_pressed = False

    fps = 200
    clock = pygame.time.Clock()

    size = width, height = 1200, 600
    speed = [2, 2]
    white = 255, 255, 255
    grey = (56, 59, 56)

    keyboardEvents = KeyboardEventHandler()
    gui.draw(play_button)

    track = Track(screen)
    car = Car(50, 60, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN and play_button.is_over(pygame.mouse.get_pos()):
                is_play_button_pressed = True
            keyboardEvents.process(event)

        if play_button.is_over(pygame.mouse.get_pos()):
            play_button.button_bg = Button.ACTIVE_COLOR
        play_button.draw(screen)

        if is_play_button_pressed:
            play_button.button_bg = Button.ACTIVE_COLOR
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
