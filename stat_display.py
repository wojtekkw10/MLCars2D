import pygame as pg
import constants
import sys

from gameObjects.button import Button


class StatBox:

    def __init__(self, win, x_pos, y_pos, width, height, padding, color=[(50, 100, 150), (50, 50, 100), (255, 255, 255), (200, 200, 255), (255, 200, 220)]):
        self.win = win
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.padding = int(height * padding)
        self.height = height
        self.width = width
        self.fitness_list = []
        self.fitness_points = []
        self.highest_fitness = 0
        self.stat_x = x_pos + self.padding
        self.stat_y = y_pos + self.padding
        self.stat_height = height - 2 * self.padding
        self.stat_width = width - 2 * self.padding
        self.hidden = False
        self.stat_button = Button(self.x_pos + self.width - 60, 265, "hide")

    def new_score(self, fitness):
        self.fitness_list.append(fitness)
        if fitness > self.highest_fitness:
            self.highest_fitness = fitness
        self.calc_positions()

    def calc_positions(self):
        fit_list = self.fitness_list
        size = len(fit_list)
        self.fitness_points = [[self.stat_x, self.stat_y + self.stat_height]]
        for i in range(size):
            fit_x = int(self.stat_x + self.stat_width * (i + 1) / size)
            fit_y = int(self.stat_y + self.stat_height *
                        (1 - fit_list[i] / self.highest_fitness))
            self.fitness_points.append([fit_x, fit_y])

    def clear_score(self):
        self.fitness_list = []
        self.fitness_points = []
        self.highest_fitness = 0

    def display(self):
        if not self.hidden:
            pg.draw.rect(
                self.win, self.color[0], (self.x_pos, self.y_pos, self.width, self.height))
            pg.draw.rect(self.win, self.color[1], (self.stat_x,
                                                   self.stat_y, self.stat_width, self.stat_height))
            pg.draw.rect(self.win, self.color[2],
                         (self.stat_x - 1, self.stat_y - 1, self.stat_width + 2, self.stat_height + 2), 3)

            for i in range(len(self.fitness_points) - 1):
                if self.fitness_points[i+1][1] - self.fitness_points[i][1] < 0:
                    pg.draw.aaline(self.win, self.color[3], (self.fitness_points[i][0], self.fitness_points[i][1]),
                                   (self.fitness_points[i + 1][0],
                                    self.fitness_points[i + 1][1]),
                                   2)
                else:
                    pg.draw.aaline(self.win, self.color[4], (self.fitness_points[i][0], self.fitness_points[i][1]), (
                        self.fitness_points[i + 1][0], self.fitness_points[i + 1][1]), 2)


# example
'''
size_ = window_width, window_height = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT
pg.init()
screen = pg.display.set_mode(size_)
clock = pg.time.Clock()

stats = StatBox(screen, 890, 10, 300, 150, 0.05)

stats.new_score(100)
stats.new_score(300)
stats.new_score(400)
stats.new_score(500)
stats.new_score(550)
stats.new_score(560)
stats.new_score(550)
stats.new_score(560)
stats.new_score(600)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    stats.display()

    pg.display.flip()
    clock.tick(60)
'''
