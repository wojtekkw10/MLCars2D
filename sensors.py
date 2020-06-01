import pygame
from math import cos, sin, sqrt
from angle import Angle

SENSOR_WIDTH_INITIAL = 90
SENSORS_COLOR_INACTIVE = pygame.Color(50, 120, 255, a=100)
SENSORS_COLOR_ACTIVE = pygame.Color(255, 90, 70, a=100)


def calculate_vector(origin, radians, sensor_size):
    return pygame.Vector2(cos(radians)*sensor_size + origin.x, sin(radians)*sensor_size + origin.y)


def determine_line_end(grid, origin, line):
    if abs(origin.x - line.x) > abs(origin.y-line.y):
        if origin.x < line.x:
            (x1, y1) = origin
            (x2, y2) = line
        else:
            (x1, y1) = line
            (x2, y2) = origin

        a = (y2 - y1) / (x2 - x1)

        for x in range(int(x1), int(x2)):
            y = a * (x - x1) + y1
            x, y = int(x), int(y)
            try:
                if grid[x, y]:  # more precise
                    return pygame.Vector2(x, y), True
            except IndexError:  # run out of track grid
                pass
    else:
        if origin.y < line.y:
            (x1, y1) = origin
            (x2, y2) = line
        else:
            (x1, y1) = line
            (x2, y2) = origin

        a = (x2 - x1) / (y2 - y1)

        for y in reversed(range(int(y1), int(y2))):
            x = a * (y - y1) + x1
            x, y = int(x), int(y)
            try:
                if grid[x, y]:  # more precise
                    return pygame.Vector2(x, y), True
            except IndexError:  # run out of track grid
                pass

    return line, False


class SensorData:
    def __init__(self, vector=(pygame.Vector2(0, 0)), detected=False, sensor_size=SENSOR_WIDTH_INITIAL):
        super().__init__()
        self.update_vector(vector)
        self.detected = detected
        self.sensor_size = sensor_size  # normal sensor_size
        # affected sensor_size (if no detection --> distance==sensor_size)
        self.distance = sensor_size

    def update_vector(self, vector):
        # print(vector)
        self.x = vector.x
        self.y = vector.y

    def update_detection_distance(self, origin):
        self.distance = sqrt(pow(abs(self.x-origin.x), 2) +
                             pow(abs(self.y-origin.y), 2))

    @property
    def detection(self):
        return self.detected, self.distance

    @property
    def vector(self):
        # print('access', pygame.Vector2(self.x, self.y))
        return pygame.Vector2(self.x, self.y)


class Sensors:

    def __init__(self, origin):
        super().__init__()
        self.lines = ['leftline2', 'leftline1',
                      'midline', 'rightline1', 'rightline2']

        self.detected = {}
        for line in self.lines:
            self.detected[line] = SensorData()

        self.origin = origin

        self.detected['midline'].sensor_size += 100
        self.detected['rightline1'].sensor_size += 70
        self.detected['leftline1'].sensor_size += 70

    def setup_sensors(self, angle, origin):
        self.origin = origin
        offset = -60
        for line in self.lines:
            self.detected[line].update_vector(calculate_vector(
                origin, -Angle(angle.degree + offset).radians, self.detected[line].sensor_size))
            offset += 30

    def check_collision(self, grid):
        for line in self.lines:
            vector, detected = determine_line_end(
                grid, self.origin, self.detected[line].vector)

            self.detected[line].update_vector(vector)
            self.detected[line].update_detection_distance(self.origin)
            self.detected[line].detected = detected

    def draw_sensors(self, surface, camera):
        origin = camera.apply_on_line(self.origin)
        for line in self.lines:
            line_vector = self.detected[line].vector
            line_vector = camera.apply_on_line(line_vector)

            start_pos = (origin.x, origin.y)
            end_pos = (line_vector.x, line_vector.y)
            if self.detected[line].detected:
                pygame.draw.aaline(surface, SENSORS_COLOR_ACTIVE, start_pos, end_pos, 2)
            else:
                pygame.draw.aaline(surface, SENSORS_COLOR_INACTIVE, start_pos, end_pos, 2)

    def get_states_of_sensors(self):
        distances = []
        for line in self.lines:
            distances.append((self.detected[line].distance, self.detected[line].detected))
        return distances
