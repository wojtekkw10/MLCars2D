from math import radians


class Angle:
    def __init__(self, angle):
        super().__init__()
        self.__angle = angle

    @property
    def degree(self):
        return self.__angle

    @degree.setter
    def degree(self, angle):
        if angle >= 360:
            self.__angle = angle % 360
        elif angle < 0:
            self.__angle = 360 - self.__angle
        else:
            self.__angle = angle

    @property
    def radians(self):
        return radians(self.__angle)
