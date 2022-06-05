
class Torpedo:

    def __init__(self, x_axis_coordinate, y_axis_coordinate, x_axis_speed, y_axis_speed, orientation):
        self.__x_axis_coordinate = x_axis_coordinate
        self.__y_axis_coordinate = y_axis_coordinate
        self.__x_axis_speed = x_axis_speed
        self.__y_axis_speed = y_axis_speed
        self.__orientation = orientation
        self.__radius = 4
        self.__life_span = 0

    # getters
    def get_x_axis_coordinate(self):
        return self.__x_axis_coordinate

    def get_y_axis_coordinate(self):
        return self.__y_axis_coordinate

    def get_x_axis_speed(self):
        return self.__x_axis_speed

    def get_y_axis_speed(self):
        return self.__y_axis_speed

    def get_orientation(self):
        return self.__orientation

    def get_radius(self):
        """"""
        return self.__radius

    def get_life_span(self):
        """"""
        return self.__life_span

    def set_location(self, new_x, new_y):
        """"""
        self.__x_axis_coordinate = new_x
        self.__y_axis_coordinate = new_y

    def reduce_life_span(self):
        self.__life_span += 1