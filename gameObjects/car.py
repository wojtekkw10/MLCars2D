import pygame
from math import cos, sin
from angle import Angle


def mapped_key(key):
    return {
        'w': pygame.K_w,
        'a': pygame.K_a,
        's': pygame.K_s,
        'd': pygame.K_d,
        'space': pygame.K_SPACE
    }.get(key)


class Car:
    DIVIDER_SPEED = 0.0001
    DIVIDER_ANGLE = 0.1

    def __init__(self, x, y):
        super().__init__()
        self.position_x = x
        self.position_y = y
        self.speed = 0.0
        self.angle = Angle(0)  # 0 is E, 90 is N, 180 is W, 270 is S
        self.max_speed = 0.03

    def handle_keyboard(self, keyboardEvents):
        if(keyboardEvents.isPressed(mapped_key('w'))):
            self.speed += 1.0 * Car.DIVIDER_SPEED
            if self.speed > self.max_speed:
                self.speed = self.max_speed
        elif (keyboardEvents.isPressed(mapped_key('s'))):
            self.speed -= 1.0 * Car.DIVIDER_SPEED
            if self.speed < -self.max_speed:
                self.speed = -self.max_speed
        elif (keyboardEvents.isPressed(mapped_key('a'))):
            self.angle.degree += 1.0 * Car.DIVIDER_ANGLE
        elif (keyboardEvents.isPressed(mapped_key('d'))):
            self.angle.degree -= 1.0 * Car.DIVIDER_ANGLE
        elif (keyboardEvents.isPressed(mapped_key('space'))):
            self.speed = 0.0

    def update(self):
        nx = cos(self.angle.radians) * self.speed
        ny = sin(self.angle.radians) * self.speed
        self.position_x += nx
        self.position_y += ny * -1.0

    def draw(self, surface):
        nx = cos(self.angle.radians) * 4
        ny = sin(self.angle.radians) * 4
        nx = self.position_x + nx + 1.5
        ny = (self.position_y - ny) + 1.5

        surface.fill((255, 0, 0), ((nx, ny), (3, 3)))  # front
        surface.fill((0, 0, 0), ((self.position_x, self.position_y), (5, 5)))
