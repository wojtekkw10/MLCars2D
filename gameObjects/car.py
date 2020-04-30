import pygame
from math import cos, sin, pi
from angle import Angle

MAX_RADIANS = 2 * pi

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

    def __init__(self, x, y, screen):
        super().__init__()

        self.image = pygame.image.load('images/car.png')
        self.car_width = self.image.get_width()
        self.car_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.screen = screen
        self.position_x = x
        self.position_y = y
        self.speed = 0.0
        self.angle = Angle(0)  # 0 is E, 90 is N, 180 is W, 270 is S
        self.car_points = {}
        self.rotate_car_points()
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
        elif (keyboardEvents.isPressed(mapped_key('space'))):
            self.speed = 0.0
        if (keyboardEvents.isPressed(mapped_key('a'))):
            self.angle.degree += 1.0 * Car.DIVIDER_ANGLE
        if (keyboardEvents.isPressed(mapped_key('d'))):
            self.angle.degree -= 1.0 * Car.DIVIDER_ANGLE


    def update(self):
        nx = cos(self.angle.radians) * self.speed
        ny = sin(self.angle.radians) * self.speed

        self.position_x += nx
        self.position_y += ny * -1


    def draw(self, surface):

        rotated = pygame.transform.rotate(self.image, self.angle.degree)
        rect = rotated.get_rect()

        position = pygame.Vector2(self.position_x, self.position_y)
        self.screen.blit(rotated, position - (rect.width/2.0, rect.height/2.0))

        self.rotate_car_points()


    def rotate_car_points(self):

        rotation_angle = MAX_RADIANS - self.angle.radians

        (fx, fy) = self.position_x + self.car_width/2, self.position_y
        self.car_points['front'] = self.get_rotated_point(fx, fy, rotation_angle)

        (flx, fly) = self.position_x + self.car_width/2.0, self.position_y - self.car_height/2.0
        self.car_points['front_left'] = self.get_rotated_point(flx, fly, rotation_angle)

        (frx, fry) = self.position_x + self.car_width/2.0, self.position_y + self.car_height/2.0
        self.car_points['front_right'] = self.get_rotated_point(frx, fry, rotation_angle)

        (rx, ry) = self.position_x - self.car_width/2, self.position_y
        self.car_points['rear'] = self.get_rotated_point(rx, ry, rotation_angle)

        (rlx, rly) = self.position_x - self.car_width/2.0, self.position_y - self.car_height/2.0
        self.car_points['rear_left'] = self.get_rotated_point(rlx, rly, rotation_angle)

        (rrx, rry) = self.position_x - self.car_width / 2.0, self.position_y + self.car_height / 2.0
        self.car_points['rear_right'] = self.get_rotated_point(rrx, rry, rotation_angle)

        (lx, ly) = self.position_x, self.position_y - self.car_height/2.0
        self.car_points['left'] = self.get_rotated_point(lx, ly, rotation_angle)

        (rx, ry) = self.position_x, self.position_y + self.car_height / 2.0
        self.car_points['right'] = self.get_rotated_point(rx, ry, rotation_angle)

    def get_rotated_point(self, x, y, angle):

        rx =  int(self.position_x + (x - self.position_x) * cos(angle) - (y - self.position_y) * sin(angle))
        ry = int(self.position_y + (x - self.position_x) * sin(angle) + (y - self.position_y) * cos(angle))
        return (rx, ry)

    def detect_collision(self, grid):

        for (x, y) in self.car_points.values():
            if y >= self.screen.get_height()-2:
                self.speed = 0
                self.position_y -= 2
            if y <= 2:
                self.speed = 0
                self.position_y += 2
            if x >= self.screen.get_width()-2:
                self.speed = 0
                self.position_x -= 2
            if x <= 2:
                self.speed = 0
                self.position_x += 2
            self.update()
            self.draw(None)

            if grid[x, y] == 1:
                return True

        return False