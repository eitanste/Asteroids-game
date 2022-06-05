#################################################################
# FILE:
# WRITER1: Eitan_Stepanov , eitanste1
# WRITER2: Tanya_Fainstein, t_fainstein
# EXERCISE: intro2cs2 ex8 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED: None
#################################################################

from screen import Screen
import sys
import random
import math
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo

DEFAULT_ASTEROIDS_NUM = 5
DELTA_X = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X
DELTA_Y = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y
SPLITEBLE_SIZES = (2, 3)
MAX_TORPEDO_ALLOWED = 10
MESSAGE_TYPE_LIFE = "life"
MESSAGE_TYPE_END_GAME = "GAME OVER"
COLLISION_MESSAGE = "OOPSIE DAISY!! BE CAREFUL!!"
MESSAGE_NO_LIVES = 'Hah! No more lives left, LOOSER!!'
MESSAGE_NO_ASTEROIDS = 'No asteroids left, you are TOTACH MIFLETZET!!'
MESSAGE_FORCE_QUITE = "Why dont you want to play...? Okay bye"
TURN_LEFT = 7
TURN_RIGHT = -7
MIN_ASTEROID_SPEED = 1
MAX_ASTEROID_SPEED = 4
MAX_ASTEROID_SIZE = 3
MED_ASTEROID_SIZE = 2
MIN_ASTEROID_SIZE = 1
POINTS_FOR_BIGG_ASTEROID = 20
POINTS_FOR_MID_ASTEROID = 50
POINTS_FOR_SMALL_ASTEROID = 100
LIMIT_LIFE_SPAN = 199
NO_LIVES_LEFT = 0


class GameRunner:

    def __init__(self, asteroids_amount=DEFAULT_ASTEROIDS_NUM):
        """This is the init of the game runner"""
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroids_amount = asteroids_amount
        self.__ship = self.__init_ship()
        self.__asteroids = self.__asteroid_initiatior(asteroids_amount)
        self.__torpedos = []
        self.__score = 0

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """This method runs the game loop.
        The most important method of the class"""

        self.__ship_manager()
        self.__asteroid_manager()
        self.__torpedo_manager()

        self.__end_game_manager()

    def __random_init(self):
        """
        This method generates a random pair of coordinates accordingly
        to the screen size
        :return: random pair of coordinates
        """
        x = random.randrange(self.__screen_min_x, self.__screen_max_x)
        y = random.randrange(self.__screen_min_y, self.__screen_max_y)
        return x, y

    def __move_objects(self, obj):
        """This method is the common method for moving(setting new location for
         the object """
        new_x = self.__screen_min_x + \
                (obj.get_x_axis_coordinate()
                 + obj.get_x_axis_speed() - self.__screen_min_x) % DELTA_X
        new_y = self.__screen_min_y + \
                (obj.get_y_axis_coordinate()
                 + obj.get_y_axis_speed() - self.__screen_min_y) % DELTA_Y
        obj.set_location(new_x, new_y)


#------------------- ship related functions ----------------------------------#

    def __ship_manager(self):
        """This method manages all operation with ship """
        self.__ship_handler()
        self.__turn_left_right()
        self.__ship_acceleration()

    def __ship_handler(self):
        """This method manages the creation and the movement of the ship"""
        self.__move_objects(self.__ship)
        x, y, orientation = self.__ship.get_full_location()
        self.__screen.draw_ship(x, y, orientation)

    def __init_ship(self):
        """
        Initiate the ship at the beginning of the game
        :return: instance of Ship
        """
        x, y = self.__random_init()
        return Ship(x, y)

    def __turn_left_right(self):
        """This method is responsible for the changing of the heading
        of the ship"""
        angle = 0
        if self.__screen.is_left_pressed():
            angle = TURN_LEFT
        if self.__screen.is_right_pressed():
            angle = TURN_RIGHT
        self.__ship.set_orientation(self.__ship.get_orientation() + angle)

    def __ship_acceleration(self):
        """This method accelerates the ship by updating it"s speed values"""
        if self.__screen.is_up_pressed():
            self.__ship.set_x_axis_speed(self.__ship.get_x_axis_speed() +
                                         (math.cos(math.radians(
                                             self.__ship.get_orientation()))))
            self.__ship.set_y_axis_speed(self.__ship.get_y_axis_speed() +
                                         (math.sin(math.radians(
                                             self.__ship.get_orientation()))))

# ------------------- asteroid related functions -----------------------------#

    def __asteroid_manager(self):
        """This method manages the asteroid operations"""
        self.__asteroid_operator()
        self.__asteroid_intersector()

    def __asteroid_initiatior(self, asteroid_num):
        """Creates the asteroids in the game, if there is some input from
        command line is uses it otherwise use the default value
        :return: list of asteroids"""
        asteroids = []
        for ast in range(asteroid_num):
            while True:
                x, y = self.__random_init()
                if x != self.__ship.get_x_axis_coordinate() \
                        or y != self.__ship.get_y_axis_coordinate():
                    break
            x_speed = random.randint(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED)
            y_speed = random.randint(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED)
            asteroid = Asteroid(x, y, x_speed, y_speed)
            self.__screen.register_asteroid(asteroid,
                                            asteroid.get_asteroid_size())

            self.__screen.draw_asteroid(asteroid, x, y)

            asteroids.append(asteroid)
        return asteroids

    def __asteroid_operator(self):
        """This method is responsible for movement of asteroids and it's
        representation on the screen"""
        for astheroid in self.__asteroids:
            self.__move_objects(astheroid)
            self.__screen.draw_asteroid(astheroid,
                                        astheroid.get_x_axis_coordinate(),
                                        astheroid.get_y_axis_coordinate())

    def __asteroid_intersector(self):
        """This method checks if there are intersection of an asteroid with the
         ship and manages the process of updating the data after the
         intersection"""
        asteroid_list = self.__asteroids[:]
        for ast in asteroid_list:
            if ast.has_intersection(self.__ship):
                self.__ship.reduce_life()
                self.__screen.remove_life()
                self.__screen.show_message(MESSAGE_TYPE_LIFE,
                                           COLLISION_MESSAGE)
                self.__screen.unregister_asteroid(ast)

                self.__asteroids.remove(ast)

    def __astroid_spliter(self, asteroid, torpedo):
        """
        Creates the asteroids after the collision accordingly to the given data
        """
        x_location = asteroid.get_x_axis_coordinate()
        y_location = asteroid.get_y_axis_coordinate()
        new_x_speed, new_y_speed = self.__new_asteroid_vel_calc(torpedo,
                                                                asteroid)
        size = asteroid.get_asteroid_size() - 1
        self.__asteroid_creator(x_location, y_location, new_x_speed,
                                new_y_speed, size)
        self.__asteroid_creator(x_location, y_location, -1 * new_x_speed,
                                -1 * new_y_speed, size)

    def __asteroid_creator(self, x, y, x_speed, y_speed, size):
        """This method manages the creation of asteroid and the
         asteroid list"""
        asteroid = Asteroid(x, y, x_speed, y_speed, size)
        self.__screen.register_asteroid(asteroid,
                                        asteroid.get_asteroid_size())

        self.__screen.draw_asteroid(asteroid, x, y)

        self.__asteroids.append(asteroid)

    def __new_asteroid_vel_calc(self, torpedo, asteroid):
        """This method calculates the speed of the asteroid that was created
         after the collision
         :returns: tuple os the speed value"""
        new_x_speed = (torpedo.get_x_axis_speed() + asteroid.get_x_axis_speed()) \
                      / math.sqrt(asteroid.get_x_axis_speed() ** 2
                         + asteroid.get_y_axis_speed() ** 2)
        new_y_speed = (torpedo.get_y_axis_speed() + asteroid.get_y_axis_speed()) \
                      / math.sqrt(asteroid.get_x_axis_speed() ** 2
                                  + asteroid.get_y_axis_speed() ** 2)
        return new_x_speed, new_y_speed

# ------------------- torpedo related functions ------------------------------#

    def __torpedo_manager(self):
        """This method manages all the operation with torpedoes"""
        self.__torpedo_creator()
        self.__torpedo_operator()
        self.__torpedo_intersector()
        self.__torpedo_life_span_manager()

    def __torpedo_speed(self):
        """
        This method defines the torpedo speed
        :return: a tuple of torpedo's speed values
        """
        torpedo_speed_x = self.__ship.get_x_axis_speed() + (
                2 * math.cos(math.radians(self.__ship.get_orientation())))
        torpedo_speed_y = self.__ship.get_y_axis_speed() + (
                2 * math.sin(math.radians(self.__ship.get_orientation())))
        return torpedo_speed_x, torpedo_speed_y

    def __torpedo_creator(self):
        """Creates torpedoes accordingly to the maximum allowed quantity"""
        if self.__screen.is_space_pressed() \
                and len(self.__torpedos) < MAX_TORPEDO_ALLOWED:
            x_torpedo, y_torpedo, x_speed, y_speed, orientation \
                = self.__torpedo_init_data()
            torpedo = Torpedo(x_torpedo, y_torpedo, x_speed, y_speed,
                              orientation)
            self.__screen.register_torpedo(torpedo)
            self.__screen.draw_torpedo(torpedo, x_torpedo, y_torpedo,
                                       orientation)
            self.__torpedos.append(torpedo)

    def __torpedo_init_data(self):
        """
        Sets the torpedo initial data
        :return: tuple of torpedo's data
        """
        x_torpedo = self.__ship.get_x_axis_coordinate()
        y_torpedo = self.__ship.get_y_axis_coordinate()
        x_speed, y_speed = self.__torpedo_speed()
        orientation = self.__ship.get_orientation()
        return x_torpedo, y_torpedo, x_speed, y_speed, orientation

    def __torpedo_operator(self):
        """ This method is responsible for movement of torpedo and it's
        representation on the screen"""
        for torpedo in self.__torpedos:
            self.__move_objects(torpedo)
            self.__screen.draw_torpedo(torpedo,
                                       torpedo.get_x_axis_coordinate(),
                                       torpedo.get_y_axis_coordinate(),
                                       torpedo.get_orientation())

    def __torpedo_intersector(self):
        """This method checks the collision of torpedoes and asteroids and
         manages the data update after the collision """
        asteroid_list = self.__asteroids[:]
        for ast in asteroid_list:
            for torpedo in self.__torpedos:
                if ast.has_intersection(torpedo):
                    self.__score_update(ast)
                    self.__torpedos.remove(torpedo)
                    self.__screen.unregister_asteroid(ast)
                    if ast.get_asteroid_size() in SPLITEBLE_SIZES:
                        self.__astroid_spliter(ast, torpedo)
                    self.__screen.unregister_torpedo(torpedo)
                    self.__asteroids.remove(ast)
                    break
            continue

    def __torpedo_life_span_manager(self):
        """ Checks the life span of torpedoes and removes relevant torpedoes
        from the screen"""
        for torpedo in self.__torpedos:
            if torpedo.get_life_span() > LIMIT_LIFE_SPAN:
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedos.remove(torpedo)
            torpedo.reduce_life_span()

    def __score_update(self, asteroid):
        """This method updates the score of the game"""
        if asteroid.get_asteroid_size() == MAX_ASTEROID_SIZE:
            self.__score += POINTS_FOR_BIGG_ASTEROID
        if asteroid.get_asteroid_size() == MED_ASTEROID_SIZE:
            self.__score += POINTS_FOR_MID_ASTEROID
        if asteroid.get_asteroid_size() == MIN_ASTEROID_SIZE:
            self.__score += POINTS_FOR_SMALL_ASTEROID
        self.__screen.set_score(self.__score)

    def __end_game_manager(self):
        """This method manages the ending of the game and shows to the user
         relevant message in the case of the game's ending"""
        message = ''
        checker = False
        if self.__ship.get_life() == NO_LIVES_LEFT:
            message = MESSAGE_NO_LIVES
            checker = True
        elif self.__asteroids == []:
            message = MESSAGE_NO_ASTEROIDS
            checker = True
        elif self.__screen.should_end():
            message = MESSAGE_FORCE_QUITE
            checker = True
        if checker:
            self.__screen.show_message(MESSAGE_TYPE_END_GAME, message)
            self.__screen.end_game()
            sys.exit()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
