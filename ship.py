class Ship():

    def __init__(self, x_axis_coordinate, y_axis_coordinate, x_axis_speed=0,
                 y_axis_speed=0, orientation=0, life=3, radius=1):
        self.__x_axis_coordinate = x_axis_coordinate
        self.__y_axis_coordinate = y_axis_coordinate
        self.__x_axis_speed = x_axis_speed
        self.__y_axis_speed = y_axis_speed
        self.__orientation = orientation
        self.__life = life
        self.__radius = radius



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
        return self.__radius

    def get_full_location(self):
        """"""
        return self.__x_axis_coordinate, \
               self.__y_axis_coordinate, \
               self.__orientation

    def get_life(self):
        """"""
        return self.__life

    def set_location(self, new_x, new_y):
        """"""
        self.__x_axis_coordinate = new_x
        self.__y_axis_coordinate = new_y

    def set_orientation(self, new_orientation):
        self.__orientation = new_orientation

    def set_x_axis_speed(self, new_x_axis_speed):
        self.__x_axis_speed = new_x_axis_speed

    def set_y_axis_speed(self, new_y_axis_speed):
        self.__y_axis_speed = new_y_axis_speed

    def reduce_life(self):
        self.__life -= 1
