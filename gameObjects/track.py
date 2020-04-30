import pygame
import numpy as np

class Track:

    green = (148, 181, 51)

    def __init__(self, screen, track_width=100):

        self.screen = screen
        self.track_width = track_width
        self.grid = np.zeros(self.screen.get_size())
        self.track_line1_points = [(0, 20)]
        self.track_line2_points = []
        self.previous_point = self.track_line1_points[0]
        self.initialize_points()


    def initialize_points(self):

        self.track_line1_points = [(0, 20),
            (466, 25), (798, 165), (1085, 176),
            (1108, 428), (894, 548), (560, 555),
            (175, 434), (3, 432)]


        self.track_line2_points = [(0, 110),
           (457, 126), (739, 248), (965, 256),
           (979, 379), (890, 450), (572, 458),
           (200, 359), (2, 342)]

        self.initialize_track_line(self.track_line1_points)
        self.initialize_track_line(self.track_line2_points)

    def initialize_track_line(self, track_line):

        for i in range(len(track_line) - 1):

            (x1, y1) = track_line[i]
            (x2, y2) = track_line[i + 1]

            a = (y2 - y1) / (x2 - x1)

            if x2 > x1:
                start, end = x1, x2
            else:
                start, end = x2, x1

            for x in range(start, end):
                y = a * (x - x1) + y1
                x, y = int(x), int(y)
                self.grid[x, y] = 1

            if y2 > y1:
                start, end = y1, y2
            else:
                start, end = y2, y1

            for y in range(start, end):
                x = (y - y1)/a + x1
                x, y = int(x), int(y)
                self.grid[x, y] = 1


    def draw_track(self):

        for i in range(len(self.track_line1_points) - 1):
            (x1, y1) = self.track_line1_points[i]
            (x2, y2) = self.track_line1_points[i + 1]
            pygame.draw.line(self.screen, self.green, (x1, y1), (x2, y2), 5)

        for i in range(len(self.track_line2_points) - 1):
            (x1, y1) = self.track_line2_points[i]
            (x2, y2) = self.track_line2_points[i + 1]
            pygame.draw.line(self.screen, self.green, (x1, y1), (x2, y2), 5)

    def add_track_point(self, point):

        pygame.draw.line(self.screen, self.green, self.previous_point, point, 5)

        self.track_line1_points.append(point)
        (x1, y1) = self.previous_point
        (x2, y2) = point

        a = (y2 - y1) / (x2 - x1)

        for x in range(x1, x2):
            y = a * (x - x1) + y1
            x, y = int(x), int(y)
            self.grid[x, y] = 1

        self.previous_point = point
