import copy
from random import Random

import numpy as np

from .action import Action
from .agent import Agent
from .state import State
from .state_with_racetrack import StateWithRacetrack


class Game:
    def __init__(self, racetrack: np.ndarray, random_state: None | int = None):
        """
        Capsules all the game logic. Mainly contains the Environment (racetrack) and Agent (car).

        :param racetrack: the racetrack on which the game should be played
        :param random_state: Used for generating the randomness of the racetrack. Pass an int for reproducible output across multiple function calls
        """
        self.rnd = Random(random_state)
        self.racetrack = racetrack
        self.reset()

    def get_n_steps(self) -> int:
        """
        Get number of steps that were done in the current game
        """
        return self.n_steps

    def reset(self) -> None:
        """
        Reset game to starting conditions
        """
        self.agent = Agent(self.rnd.choice(self.__get_start_cells()), (0, 0))
        self.n_steps = 0

    def is_finished(self) -> bool:
        """
        Returns if the game is finished, which means that the agent reached the finish line.
        """
        if self.agent.pos in self.__get_end_cells():
            return True
        return False

    def noisy_step(self, action: Action) -> int:
        """
        Applies the specified action to the environment. With certain probability the action is ignored (= noise).

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

        # create new velocity. If it is valid, set the agent velocity to the new velocity
        self.agent.vel = self.__check_velocity((action.x, action.y))

        # create new position. If it is valid, set the agent position to the new position
        self.agent.pos, has_been_reset = self.__check_pos()

        # return reward
        if has_been_reset:
            return -5
        return -1

    def __check_pos(self):
        """
        Checks if the position is still valid after applying the velocity. If it is valid the new position is
        returned, else the old one is returned.

        :return: Returns new position if it is valid, else it returns the old one
        """
        new_pos = (self.agent.pos[0] + self.agent.vel[0],
                   self.agent.pos[1] + self.agent.vel[1])

        # reset if it cuts corners
        if self.__check_intersect(self.agent.pos, new_pos):
            self.agent.reset_velocity()
            self.agent.pos = self.rnd.choice(self.__get_start_cells())
            return self.agent.pos, True

        # checking if it is out of bounds
        # car can't move out of the grid.
        out_of_bound = False
        if new_pos[0] >= self.racetrack.shape[0]:
            self.agent.reset_velocity()
            new_pos = (self.racetrack.shape[0] - 1, new_pos[1])
            out_of_bound = True
        if new_pos[0] < 0:
            self.agent.reset_velocity()
            new_pos = (0, new_pos[1])
            out_of_bound = True
        if new_pos[1] >= self.racetrack.shape[1]:
            self.agent.reset_velocity()
            new_pos = (new_pos[0], self.racetrack.shape[1] - 1)
            out_of_bound = True
        if new_pos[1] < 0:
            self.agent.reset_velocity()
            new_pos = (new_pos[0], 0)
            out_of_bound = True

        if out_of_bound:
            if self.racetrack[new_pos[0]][new_pos[1]] != 3:
                # reset agents starting position and velocity
                self.agent = Agent(self.rnd.choice(self.__get_start_cells()), (0, 0))
                return self.agent.pos, True

        # checking if it is on an invalid cell
        if self.racetrack[new_pos[0]][new_pos[1]] == 0:
            self.agent.reset_velocity()
            self.agent.pos = self.rnd.choice(self.__get_start_cells())
            return self.agent.pos, True

        return new_pos, False

    def __check_intersect(self, old_pos, new_pos):
        x_distance = new_pos[0] - old_pos[0]
        y_distance = new_pos[1] - old_pos[1]
        old_pos = copy.deepcopy(old_pos)

        while x_distance > 0 or y_distance > 0:
            if x_distance > 0:
                x_distance -= 1
                old_pos = (old_pos[0] + 1, old_pos[1])
            if y_distance > 0:
                y_distance -= 1
                old_pos = (old_pos[0], old_pos[1] + 1)

            if old_pos[0] >= self.racetrack.shape[0]:
                old_pos = (self.racetrack.shape[0] - 1, old_pos[1])
            if old_pos[1] >= self.racetrack.shape[1]:
                old_pos = old_pos[0], (self.racetrack.shape[1] - 1)

            if self.racetrack[old_pos[0]][old_pos[1]] == 0:
                return True
        return False

    def __check_velocity(self, vel_change):
        """
        Checks if the velocity is still valid after changing it according to the input. If it is valid the new velocity
        is returned, else the old one is returned.

        :param vel_change: Changes to the velocity
        :return: New velocity if it is valid, else it returns the old one
        """
        # checks if velocity is not changed by more than +-1
        allowed = [-1, 0, 1]
        if vel_change[0] not in allowed or vel_change[1] not in allowed:
            print("Cannot modify velocity by more then +-1")
            return self.agent.vel

        new_vel = (self.agent.vel[0] + vel_change[0], self.agent.vel[1] + vel_change[1])

        # velocity cant be 0
        if new_vel[0] == 0 and new_vel[1] == 0:
            return (1, 0)

        # checks if velocity is >= 0 and < 5
        if new_vel[0] > 4 or new_vel[0] < -4 or new_vel[1] > 4 or new_vel[1] < -4:
            # print("Exceeded Velocity limits")
            # velocity cant be 0
            if self.agent.vel[0] == 0 and self.agent.vel[1] == 0:
                return (1, 0)
            return self.agent.vel

        return new_vel

    def get_state(self) -> State:
        """
        Get the current state of the game

        :return: Current state
        """
        return State(self.agent.pos, self.agent.vel)

    def get_state_with_racetrack(self) -> StateWithRacetrack:
        """
        Get the current state of the game including the racetrack

        :return: Current state with racetrack
        """
        return StateWithRacetrack(self.racetrack, self.agent.pos, self.agent.vel)

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
