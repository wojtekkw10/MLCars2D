from angle import Angle
import pygame
from math import cos, sin, sqrt, floor

from neural_network import CarNeuralNetwork
from sensors import Sensors
import constants


def mapped_key(key):
    return {
        'w': pygame.K_w,
        'a': pygame.K_a,
        's': pygame.K_s,
        'd': pygame.K_d,
        'space': pygame.K_SPACE
    }.get(key)


def get_line_points(point1, point2):

    (x1, y1), (x2, y2) = point1, point2

    if x1 != x2:
        a = (y2 - y1) / (x2 - x1)

        if x2 > x1:
            start, end = x1, x2
        else:
            start, end = x2, x1

        for x in range(start, end):
            y = int(a * (x - x1) + y1)
            yield (x, y)

    elif y1 != y2:

        a = (x2 - x1) / (y2 - y1)

        if y2 > y1:
            start, end = y1, y2
        else:
            start, end = y2, y1

        for y in range(start, end):
            x = int(a * (y - y1) + x1)
            yield (x, y)


def scale_to_bounds(lower, upper, sensor_states):
    scaled_distances = []
    for state in sensor_states:
        distance = state[0]
        scaled_distances.append((distance+lower)/upper)
    return scaled_distances


class Car:

    def __init__(self, x, y, screen):
        super().__init__()

        self.image = pygame.image.load('resources/images/car.png')
        self.car_width = self.image.get_width()
        self.car_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.screen = screen
        self.position_x = x
        self.position_y = y
        self.angle = Angle(0)  # 0 is E, 90 is N, 180 is W, 270 is S
        self.car_points = {}
        self.speed = constants.CAR_SPEED
        self.turn = 0.0  # axis [-1.0,1.0]
        self.sensors = Sensors(pygame.Vector2(x, y))
        self.neural_network = CarNeuralNetwork(1, [6, 4, 1])
        self.distance_traveled = 0
        self.collision_happened = False

        self.distance_counter = 0
        self.should_check_collisions = True

    def handle_neural_network(self):
        nn_input = self.get_nn_input_from_sensors()
        output = self.neural_network.calc(nn_input)
        self.update_turn_based_on_nn(output)

    def get_nn_input_from_sensors(self):
        sensor_distances = self.sensors.get_states_of_sensors()
        sensor_distances = scale_to_bounds(0, 100, sensor_distances)
        sensor_distances.append(1.0)
        sensor_distances = [3.8 - value for value in sensor_distances]
        return sensor_distances

    def update_turn_based_on_nn(self, nn_output):
        threshold = 0.7
        if nn_output < threshold:
            self.turn = 2*nn_output
        else:
            self.turn = 2*(-nn_output+threshold)

    def fixed_update(self):
        self.angle.degree -= constants.DIVIDER_ANGLE * self.turn

        nx = cos(self.angle.radians) * self.speed
        ny = sin(self.angle.radians) * self.speed

        self.position_x += nx
        self.position_y += ny * -1
        self.rect[0] = self.position_x
        self.rect[1] = self.position_y

        dst = sqrt(nx**2 + ny**2)
        self.distance_traveled += dst
        self.distance_counter += dst
        if self.distance_counter > constants.DISTANCE_TO_TRIGGER_CHECKS:
            self.distance_counter = 0
            self.should_check_collisions = True

    def update(self, camera):
        if self.collision_happened:
            return

        self.fixed_update()

        (x, y, w, h) = camera.apply(self)
        rotated = pygame.transform.rotate(self.image, self.angle.degree)
        rect = rotated.get_rect().move(pygame.Vector2(x - w / 2, y - h / 2))
        self.car_center_x, self.car_center_y = rect.center
        self.rotate_car_points()

        if self.should_check_collisions:
            self.sensors.setup_sensors(
                self.angle, pygame.Vector2(self.car_center_x, self.car_center_y))

    def draw(self, surface, camera, other_cars):
        if len(other_cars) < 15:
            if self.check_if_drawn(other_cars):
                return False

        rotated = pygame.transform.rotate(self.image, self.angle.degree)
        image_dest = pygame.Vector2(self.position_x - self.car_width / 2,
                                    self.position_y - self.car_height / 2)
        self.screen.blit(rotated, image_dest)

        self.sensors.draw_sensors(surface, camera)
        return True

    def check_if_drawn(self, cars):
        for car in cars:
            if floor(car.position_x) == floor(self.position_x) and floor(car.position_y) == floor(self.position_y):
                return True

        return False

    def rotate_car_points(self):

        rotation_angle = constants.MAX_RADIANS - self.angle.radians

        (flx, fly) = self.car_center_x + self.car_width / \
            2.0, self.car_center_y - self.car_height / 2.0
        self.car_points['front_left'] = self.get_rotated_point(
            flx, fly, rotation_angle)

        (frx, fry) = self.car_center_x + self.car_width / \
            2.0, self.car_center_y + self.car_height / 2.0
        self.car_points['front_right'] = self.get_rotated_point(
            frx, fry, rotation_angle)

        (rlx, rly) = self.car_center_x - self.car_width / \
            2.0, self.car_center_y - self.car_height / 2.0
        self.car_points['rear_left'] = self.get_rotated_point(
            rlx, rly, rotation_angle)

        (rrx, rry) = self.car_center_x - self.car_width / \
            2.0, self.car_center_y + self.car_height / 2.0
        self.car_points['rear_right'] = self.get_rotated_point(
            rrx, rry, rotation_angle)

    def get_rotated_point(self, x, y, angle):
        rx = int(self.car_center_x + (x - self.car_center_x) *
                 cos(angle) - (y - self.car_center_y) * sin(angle))
        ry = int(self.car_center_y + (x - self.car_center_x) *
                 sin(angle) + (y - self.car_center_y) * cos(angle))
        return rx, ry

    def detect_collision(self, grid, sectors):
        if not self.collision_happened and self.should_check_collisions:
            self.sensors.check_collision(grid, sectors)

        if self.should_check_collisions:
            self.should_check_collisions = False

            end_points = [(self.car_points['front_left'], self.car_points['rear_left']),
                          (self.car_points['front_left'],
                           self.car_points['front_right']),
                          (self.car_points['front_right'],
                           self.car_points['rear_right']),
                          (self.car_points['rear_left'], self.car_points['rear_right'])]

            for end_point in end_points:
                for point in get_line_points(end_point[0], end_point[1]):
                    if self.is_within_bounds(point):
                        return True

                    (x, y) = point
                    x_sector = x // constants.X_SECTOR_SIZE
                    y_sector = y // constants.Y_SECTOR_SIZE
                    if (x, y) in sectors[y_sector][x_sector]:
                        self.collision_happened = True
                        return True

        return False

    def is_within_bounds(self, point):
        is_within_bounds = False
        (x, y) = point
        if y >= self.screen.get_height() - 2:
            self.position_y -= 2
            is_within_bounds = True
        if y <= 2:
            self.position_y += 2
            is_within_bounds = True
        if x >= self.screen.get_width() - 2:
            self.position_x -= 2
            is_within_bounds = True
        if x <= 2:
            self.position_x += 2
            is_within_bounds = True

        if is_within_bounds:
            self.speed = 0
            self.distance_traveled -= 2

        return is_within_bounds
