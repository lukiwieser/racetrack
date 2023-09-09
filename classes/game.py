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

    def reset(self) -> None:
        """
        Reset game to starting conditions
        """
        self.agent = Agent(self.rnd.choice(self.__get_start_cells()), (0, 0))
        self.n_steps = 0

    def is_finished(self) -> bool:
        """
        Returns if the game is finished. This means that the agent reached the finish line.
        """
        return self.agent.pos in self.__get_end_cells()

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
        return State(self.agent.pos, self.agent.vel)

    def get_state_with_racetrack(self) -> StateWithRacetrack:
        """
        Get the current state of the game including the racetrack

        :return: Current state with racetrack
        """
        return StateWithRacetrack(self.racetrack, self.agent.pos, self.agent.vel)

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

        # apply velocity change & update position
        self.__update_velocity((action.x, action.y))
        has_been_reset = self.__update_position()

        # return reward
        return -5 if has_been_reset else -1

    def __update_position(self) -> bool:
        """
        Updates the position of the agent by adding the current velocity.
        If the new position is invalid, it will be reset to a random position on the start-line.

        Invalid positions are:
        (1) if the agent cuts corners
        (2) the agent is outside the track
        (3) the agent would be outside the map

        :return: Returns if the agents position has been reset or not.
        """
        new_pos = (self.agent.pos[0] + self.agent.vel[0],
                   self.agent.pos[1] + self.agent.vel[1])

        # reset if it cuts corners
        if self.__check_intersect(self.agent.pos, new_pos):
            self.agent.reset_velocity()
            self.agent.pos = self.rnd.choice(self.__get_start_cells())
            return True

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

        # reset agent, if out of bounds & not at finish-line
        if out_of_bound and self.racetrack[new_pos[0]][new_pos[1]] != 3:
            self.agent = Agent(self.rnd.choice(self.__get_start_cells()), (0, 0))
            return True

        # checking if it is on an invalid cell
        if self.racetrack[new_pos[0]][new_pos[1]] == 0:
            self.agent.reset_velocity()
            self.agent.pos = self.rnd.choice(self.__get_start_cells())
            return True

        # new position is valid
        self.agent.pos = new_pos
        return False

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

    def __update_velocity(self, vel_change: tuple[int, int]) -> None:
        """
        Applies the velocity-change to the agents' velocity.
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
        new_vel = (self.agent.vel[0] + vel_change[0], self.agent.vel[1] + vel_change[1])

        # velocity must be >= 0 and <= 4
        if new_vel[0] > 4 or new_vel[0] < -4 or new_vel[1] > 4 or new_vel[1] < -4:
            new_vel = self.agent.vel

        # velocity cannot be 0
        if new_vel[0] == 0 and new_vel[1] == 0:
            new_vel = (1, 0)

        # set new velocity
        self.agent.vel = new_vel

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
