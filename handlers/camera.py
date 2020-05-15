import pygame
from pygame import *


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def apply_on_rect(self, target):
        return target.move(self.state.topleft)

    def apply_on_line(self, line):
        line = pygame.Vector2(line.x + self.state.x, line.y + self.state.y)
        return line

    def update(self, target):
        # print(self.state.topleft)
        self.state = self.camera_func(self.state, target.rect)
