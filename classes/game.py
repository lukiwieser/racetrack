from random import Random

import numpy as np

from .action import Action
from .car import Car
from .state import State
from .state_with_racetrack import StateWithRacetrack


class Game:
    def __init__(self, racetrack: np.ndarray, random_state: None | int = None):
        """
        Capsules all the game logic.
        Mainly contains the racetrack and car.

        :param racetrack: the racetrack on which the game should be played
        :param random_state: Used for generating the randomness of the racetrack. Pass an int for reproducible output across multiple function calls
        """
        self.rnd = Random(random_state)
        self.racetrack = racetrack
        self.reset()

    def reset(self) -> None:
        """
        Reset game to starting conditions
        """
        self.car = Car(self.rnd.choice(self.__get_start_cells()), (0, 0))
        self.n_steps = 0

    def is_finished(self) -> bool:
        """
        Returns if the game is finished. This means that the car reached the finish line.
        """
        return self.car.pos in self.__get_end_cells()

    def get_n_steps(self) -> int:
        """
        Get number of steps that were done in the current game
        """
        return self.n_steps

    def get_state(self) -> State:
        """
        Get the current state of the game

        :return: Current state
        """
        return State(self.car.pos, self.car.vel)

    def get_state_with_racetrack(self) -> StateWithRacetrack:
        """
        Get the current state of the game including the racetrack

        :return: Current state with racetrack
        """
        return StateWithRacetrack(self.racetrack, self.car.pos, self.car.vel)

    def noisy_step(self, action: Action) -> int:
        """
        Applies the specified action to the environment.
        With a certain probability, the action is ignored (= noise).

        :param action: indicates how the velocity should be changed
        :return: returns a reward
        """
        if self.rnd.random() >= 0.9:
            action = Action(0, 0)
        return self.step(action)

    def step(self, action: Action) -> int:
        """
        Applies the specified action to the environment.

        :param action: indicates how the velocity should be changed
        :return: returns a reward
        """

        self.n_steps += 1

        # apply velocity change & update position
        self.__update_velocity((action.x, action.y))
        has_been_reset = self.__update_position()

        # return reward
        return -5 if has_been_reset else -1

    def __update_position(self) -> bool:
        """
        Updates the position of the car by adding the current velocity.
        If the new position is invalid, it will be reset to a random position on the start-line.

        Invalid positions are:
        (1) if the car cuts corners
        (2) the car is outside the track
        (3) the car would be outside the map

        :return: Returns True if the cars position has been reset or not.
        """
        new_pos = (self.car.pos[0] + self.car.vel[0],
                   self.car.pos[1] + self.car.vel[1])

        # checking if it is out of bounds
        # car can't move out of the grid.
        out_of_bound = False
        if new_pos[0] >= self.racetrack.shape[0]:
            self.car.reset_velocity()
            new_pos = (self.racetrack.shape[0] - 1, new_pos[1])
            out_of_bound = True
        if new_pos[0] < 0:
            self.car.reset_velocity()
            new_pos = (0, new_pos[1])
            out_of_bound = True
        if new_pos[1] >= self.racetrack.shape[1]:
            self.car.reset_velocity()
            new_pos = (new_pos[0], self.racetrack.shape[1] - 1)
            out_of_bound = True
        if new_pos[1] < 0:
            self.car.reset_velocity()
            new_pos = (new_pos[0], 0)
            out_of_bound = True

        # reset car, if out of bounds & not at finish-line
        if out_of_bound and self.racetrack[new_pos[0]][new_pos[1]] != 3:
            self.car = Car(self.rnd.choice(self.__get_start_cells()), (0, 0))
            return True

        # reset if it cuts corners
        if self.__check_intersect(self.car.pos, new_pos):
            self.car.reset_velocity()
            self.car.pos = self.rnd.choice(self.__get_start_cells())
            return True

        # checking if it is on an invalid cell
        if self.racetrack[new_pos[0]][new_pos[1]] == 0:
            self.car.reset_velocity()
            self.car.pos = self.rnd.choice(self.__get_start_cells())
            return True

        # new position is valid
        self.car.pos = new_pos
        return False

    def __check_intersect(self, pos0: tuple[int, int], pos1: tuple[int, int]) -> bool:
        """
        Checks if there are any invalid cells between two specified positions using "Bresenham's Line Algorithm".
        This is done by following a line between the positions and checking its path for invalid cells.

        :returns: True if invalid cells exist between the positions, otherwise False.
        """

        # Examples if there are invalid cells between the positions:
        # ░ are valid cells, representing the racetrack
        # █ are invalid cells, representing the boundaries
        # x are the two positions of the car (pos0 & pos1)
        #
        # █ █ █ █ █ █   █ █ █ █ █ █   █ █ █ █ █ █   █ █ █ █ █ █
        # █ ░ ░ ░ ░ ░   █ ░ ░ ░ ░ ░   █ ░ ░ ░ ░ ░   █ ░ ░ ░ ░ ░
        # █ ░ ░ x ░ ░   █ ░ ░ x ░ ░   █ ░ ░ x ░ ░   █ ░ ░ ░ x ░
        # █ ░ x █ █ █   █ ░ ░ █ █ █   █ ░ ░ █ █ █   █ ░ ░ █ █ █
        # █ ░ ░ █       █ ░ x █       █ ░ ░ █       █ ░ x █
        # █ ░ ░ █       █ ░ ░ █       █ ░ x █       █ ░ ░ █
        # => False      => False      => True      => True

        x0, y0 = pos0
        x1, y1 = pos1

        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        error = dx + dy

        while True:
            if self.racetrack[x0][y0] == 0:
                return True

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * error
            if e2 >= dy:
                if x0 == x1:
                    break
                error += dy
                x0 += sx
            if e2 <= dx:
                if y0 == y1:
                    break
                error += dx
                y0 += sy

        return False

    def __update_velocity(self, vel_change: tuple[int, int]) -> None:
        """
        Applies the velocity-change to the cars' velocity.
        If the new velocity is to large/small it will be capped at the maximum/minimum.
        If the new velocity is 0, the velocity will be set to (1, 0)

        :param vel_change: Changes to the velocity
        """

        # velocity-change must be between -1 and 1
        allowed = [-1, 0, 1]
        if vel_change[0] not in allowed or vel_change[1] not in allowed:
            print("Cannot modify velocity by more then +-1")
            return

        # determine new velocity
        new_vel = (self.car.vel[0] + vel_change[0], self.car.vel[1] + vel_change[1])

        # velocity must be >= 0 and <= 4
        if new_vel[0] > 4 or new_vel[0] < -4 or new_vel[1] > 4 or new_vel[1] < -4:
            new_vel = self.car.vel

        # velocity cannot be 0
        if new_vel[0] == 0 and new_vel[1] == 0:
            new_vel = (1, 0)

        # set new velocity
        self.car.vel = new_vel

    def __get_start_cells(self) -> list[tuple[int, int]]:
        """
        Gets the coordinates (x,y) for all start cells, aka the start-line.

        :return: Returns end cells as tuples
        """
        return [tuple(coord) for coord in np.argwhere(self.racetrack == 2).tolist()]

    def __get_end_cells(self) -> list[tuple[int, int]]:
        """
        Gets the coordinates (x,y) for all end cells, aka the finish-line.

        :return: Returns end cells as tuples
        """
        return [tuple(coord) for coord in np.argwhere(self.racetrack == 3).tolist()]
