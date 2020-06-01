import pygame
import numpy as np
import constants
import files_ops


class Track:

    def __init__(self, screen, track_width=100):
        self.screen = screen
        self.track_width = track_width
        self.grid = np.zeros(self.screen.get_size())
        self.track_line1_points = [(0, 20)]
        self.track_line2_points = []
        # self.previous_point = self.track_line1_points[0]
        self.sectors = [[[] for _ in range(constants.X_SECTOR_NO)] for _ in range(constants.Y_SECTOR_NO)]
        self.initialize_points()
        self.position = (0, 0)

    def initialize_points(self, is_default_map=True):
        line1 = []
        line2 = []

        if is_default_map:
            line1 = [(0, 20),
                     (466, 25), (798, 165), (1085, 176),
                     (1108, 428), (894, 548), (560, 555),
                     (175, 434), (3, 432)]
            line2 = [(0, 110),
                     (457, 126), (739, 248), (965, 256),
                     (979, 379), (890, 450), (572, 458),
                     (200, 359), (2, 342)]
        else:
            loaded_map = files_ops.load_map()
            start_positions = loaded_map[:len(loaded_map) // 2]
            end_positions = loaded_map[len(loaded_map) // 2:]

            line1.append(start_positions[1])
            for i in range(1, len(end_positions) // 2 + 1):
                line1.append(end_positions[i])

            line2.append(start_positions[len(start_positions) // 2 + 1])
            for i in range(len(end_positions) // 2 + 1, len(end_positions)):
                line2.append(end_positions[i])

        self.track_line1_points = line1
        self.track_line2_points = line2

    def initialize_line_sector(self, point1, point2):
        (x1, y1) = point1
        (x2, y2) = point2

        a = (y2 - y1) / (x2 - x1)

        if x2 > x1:
            start, end = x1, x2
        else:
            start, end = x2, x1

        for x in range(start, end):
            y = a * (x - x1) + y1
            x, y = int(x), int(y)
            self.grid[x, y] = 1
            x_sector = x // constants.X_SECTOR_SIZE
            y_sector = y // constants.Y_SECTOR_SIZE
            self.sectors[y_sector][x_sector].append((x, y))

        if y2 > y1:
            start, end = y1, y2
        else:
            start, end = y2, y1

        for y in range(start, end):
            a = (x2 - x1) / (y2 - y1)
            x = a * (y - y1) + x1
            x, y = int(x), int(y)
            self.grid[x, y] = 1
            x_sector = x // constants.X_SECTOR_SIZE
            y_sector = y // constants.Y_SECTOR_SIZE
            self.sectors[y_sector][x_sector].append((x, y))



    def draw_track(self, camera):
        track_line_color = (62, 67, 74)
        line_thickness = 7

        if self.position != camera.get_position:
            self.sectors = [[[] for _ in range(constants.X_SECTOR_NO)] for _ in range(constants.Y_SECTOR_NO)]

        self.draw_line_segment(self.track_line1_points, camera, track_line_color, line_thickness)
        self.draw_line_segment(self.track_line2_points, camera, track_line_color, line_thickness)

        if self.position != camera.get_position:
            self.position = camera.get_position()

    def draw_line_segment(self, points, camera, line_color, line_thickness):
        for i in range(len(points) - 1):
            (x1, y1) = points[i]
            (x1, y1, _, _) = camera.apply_on_rect(pygame.Rect(x1, y1, 0, 0))
            (x2, y2) = points[i + 1]
            (x2, y2, _, _) = camera.apply_on_rect(pygame.Rect(x2, y2, 0, 0))
            pygame.draw.line(self.screen, line_color, (x1, y1), (x2, y2), line_thickness)

            if self.position != camera.get_position:
                self.initialize_line_sector((x1, y1), (x2, y2))
