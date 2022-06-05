import math


DEFAULT_SIZE = 3

class Asteroid:

    def __init__(self, x_axis_coordinate, y_axis_coordinate, x_axis_speed,
                 y_axis_speed, asteroid_size=DEFAULT_SIZE):
        self.__x_axis_coordinate = x_axis_coordinate
        self.__y_axis_coordinate = y_axis_coordinate
        self.__x_axis_speed = x_axis_speed
        self.__y_axis_speed = y_axis_speed
        self.__asteroid_size = asteroid_size

    # getters


    def get_x_axis_coordinate(self):
        return self.__x_axis_coordinate

    def get_y_axis_coordinate(self):
        return self.__y_axis_coordinate

    def get_x_axis_speed(self):
        return self.__x_axis_speed

    def get_y_axis_speed(self):
        """"""
        return self.__y_axis_speed

    def get_asteroid_size(self):
        """"""
        return self.__asteroid_size

    def get_radius(self):
        """"""
        return self.__asteroid_size * 10 - 5

    def set_location(self, new_x, new_y):
        """"""
        self.__x_axis_coordinate = new_x
        self.__y_axis_coordinate = new_y

    def has_intersection(self, obj):
        """"""
        distance = math.sqrt((obj.get_x_axis_coordinate() -
                              self.__x_axis_coordinate) ** 2 +
                             (obj.get_y_axis_coordinate() -
                              self.__y_axis_coordinate) ** 2)
        if distance <= self.get_radius() + obj.get_radius():
            return True
        return False
