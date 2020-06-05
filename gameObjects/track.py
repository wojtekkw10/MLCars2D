import pygame
import constants
import files_ops
from gameObjects.button import Button

class Track:

    def __init__(self, screen, track_width=100):
        self.screen = screen
        self.track_width = track_width
        self.track_line1_points = [(0, 20)]
        self.track_line2_points = []
        # self.previous_point = self.track_line1_points[0]
        self.sectors = [[[] for _ in range(constants.X_SECTOR_NO)] for _ in range(constants.Y_SECTOR_NO)]
        self.initialize_points()
        self.camera_state = (0, 0)
        self.back_button = Button(2140, 265, "Back")
        self.stat_button = Button(2430, 80, "Hide")

        self.position = (0, 0)


    def initialize_points(self, is_default_map=True):

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
            mapa = files_ops.load_map()
            line1, line2 = prepare_lines(mapa)


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

        self.back_button.draw(self.screen)
        self.stat_button.button_width = 100
        self.stat_button.button_height = 45
        self.stat_button.font_size = constants.SMALL_FONT
        self.stat_button.draw(self.screen)

def prepare_lines(mapa):
    half = mapa.index(constants.HALF)
    line1 = mapa[:half]
    line2 = mapa[half + 1:]

    for i in range(0, len(line1) - 2):
        if line1[i][0] == line1[i + 1][0]:
            line1.remove(line1[i])

    for i in range(0, len(line2) - 2):
        if line2[i][0] == line2[i + 1][0]:
            line2.remove(line2[i])

    return line1, line2

# def add_track_point(self, point):
#
#     pygame.draw.line(self.screen, self.green,
#                      self.previous_point, point, 5)
#
#     self.track_line1_points.append(point)
#     (x1, y1) = self.previous_point
#     (x2, y2) = point
#
#     a = (y2 - y1) / (x2 - x1)
#
#     for x in range(x1, x2):
#         y = a * (x - x1) + y1
#         x, y = int(x), int(y)
#         self.grid[x, y] = 1
#
#     self.previous_point = point

