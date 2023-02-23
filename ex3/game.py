import numpy as np
from state import State
from state_with_racetrack import StateWithRacetrack
from display import Display
from state import State
from action import Action
import random
import copy

class Game:
    def __init__(self, racetrack: np.ndarray, visualize = False):
        self.racetrack = racetrack
        self.visualize = visualize

        self.reset()

        # initalize the visualizer
        if visualize:
            state = StateWithRacetrack(self.racetrack, self.agent.pos, self.agent.vel)
            self.display = Display(state)


    def reset(self):
        # initialize Agent with starting position and velocity
        self.agent = self.Agent(random.choice(self.get_start_cells()), (0, 0))  # TODO maybe randomize at which starting cell the agent starts

    def is_finished(self):
        if self.agent.pos in self.get_end_cells():
            return True
        return False

    def step(self, action: Action) -> int:
        """
        TODO do

        :param game_input: This represents the input of the user/agent and indicates how the velocity should be changed
        :return: returns current state. # TODO finish comment
        """
        # TODO maybe introduce a limit to the velocity, like the article?
        # TODO is the car allowed to drive backwards?

        # create new velocity. If it is valid, set the agent velocity to the new velocity
        self.agent.vel = self.check_velocity((action.x, action.y))

        # create new position. If it is valid, set the agent position to the new position
        self.agent.pos = self.check_pos()

        if self.visualize:
            self.display.update_agent(self.agent.pos)

        # return reward
        return -1

    def check_pos(self):
        """
        Checks if the position is still valid after applying the velocity. If it is valid the new position is
        returned, else the old one is returned.

        :return: Returns new position if it is valid, else it returns the old one
        """
        new_pos = (self.agent.pos[0] + self.agent.vel[0], self.agent.pos[1] + self.agent.vel[1]) # self.agent.pos[1] + self.agent.vel[1]

        # reset if it cuts corners
        if self.check_intersect(self.agent.pos, new_pos):
            self.agent.reset_velocity()
            self.agent.pos = random.choice(self.get_start_cells())
            return self.agent.pos

        # checking if it is out of bounds
        # car cant move out of the grid.
        if new_pos[0] >= self.racetrack.shape[0]:
            self.agent.reset_velocity()
            new_pos = (self.racetrack.shape[0]-1, new_pos[1])
            if self.racetrack[new_pos[0]][new_pos[1]] != 3:
                self.reset()
                return self.agent.pos
        if new_pos[0] < 0:
            self.agent.reset_velocity()
            new_pos = (0, new_pos[1])
            if self.racetrack[new_pos[0]][new_pos[1]] != 3:
                self.reset()
                return self.agent.pos
        if new_pos[1] >= self.racetrack.shape[1]:
            self.agent.reset_velocity()
            new_pos = (new_pos[0], self.racetrack.shape[1]-1)
            if self.racetrack[new_pos[0]][new_pos[1]] != 3:
                self.reset()
                return self.agent.pos
        if new_pos[1] < 0:
            self.agent.reset_velocity()
            new_pos = (new_pos[0], 0)
            if self.racetrack[new_pos[0]][new_pos[1]] != 3:
                self.reset()
                return self.agent.pos

        # checking if it is on an invalid cell
        if self.racetrack[new_pos[0]][new_pos[1]] == 0:
            self.agent.reset_velocity()
            self.agent.pos = random.choice(self.get_start_cells())
            return self.agent.pos                      # TODO maybe send car back to start, instead of keeping the current position?

        # if is has not returned yet, the position is valid
        return new_pos

    def check_intersect(self, old_pos, new_pos):
        # pass
        x_distance = new_pos[0] - old_pos[0]
        y_distance = new_pos[1] - old_pos[1]
        old_pos = copy.deepcopy(old_pos)

        while x_distance > 0 or y_distance > 0:
            if x_distance > 0:
                x_distance-= 1
                old_pos = (old_pos[0]+1, old_pos[1])
            if y_distance > 0:
                y_distance-=1
                old_pos = (old_pos[0], old_pos[1]+1)

            if old_pos[0] >= self.racetrack.shape[0]:
                old_pos = (self.racetrack.shape[0]-1, old_pos[1])
            if old_pos[1] >= self.racetrack.shape[1]:
                old_pos = old_pos[0], (self.racetrack.shape[1]-1)

            if self.racetrack[old_pos[0]][old_pos[1]] == 0:
                # print("intersect")
                return True
        return False


    def check_velocity(self, vel_change):
        """
        Checks if the velocity is still valid after changing it according to the input. If it is valid the new velocity
        is returned, else the old one is returned.

        :param vel_change: Changes to the velocity
        :return: Returns new velocity if it is valid, else it returns the old one
        """
        # checks if velocity is not changed by more than +-1
        allowed = [-1, 0, 1]
        if vel_change[0] not in allowed or vel_change[1] not in allowed:
            print("Cannot modify velicity by more then +-1")
            return self.agent.vel

        new_vel = (self.agent.vel[0] + vel_change[0], self.agent.vel[1] + vel_change[1])

        # velocity cant be 0
        if new_vel[0] == 0 and new_vel[1] == 0:
            return (1, 0)

        # checks if velocity is >= 0 and < 5
        if new_vel[0] > 4 or new_vel[0] < 0 or new_vel[1] > 4 or new_vel[1] < 0:
            # print("Exceeded Velocity limits")
            # velocity cant be 0
            if self.agent.vel[0] == 0 and self.agent.vel[1] == 0:
                return (1, 0)
            return self.agent.vel

        return new_vel

    def get_state(self) -> State:
        """
        Returns the current state of the game

        :return: returns current state.
        """
        return State(self.agent.pos, self.agent.vel)

    def get_start_cells(self):
        """
        Finds all start rectangles.

        :return: Returns all starting reactangles as a list of tuples, where each tuple represents one rectangle
        """
        start_array = np.where(self.racetrack == 2)
        return self.convert(start_array)

    def get_end_cells(self):
        """
        Finds all end rectangles.

        :return: Returns all end reactangles as a list of tuples, where each tuple represents one rectangle
        """
        end_array = np.where(self.racetrack == 3)
        return self.convert(end_array)

    def convert(self, input_tuple):
        """
        Converts a tuple of 2 ndarrays to a list of tuples. This is a help function to find start/end rectangles.
        E.g. Input ([0,0,0],[4,5,6]) --> Output [(0,4),(0,5),(0,6)], where each tuple is one rectangle

        :param input_tuple: the tupl
        :return: Returns a list of tuples, where each tuple represents a rectangle
        """
        list = []
        for i in range(len(input_tuple[0])):
            list.append((input_tuple[0][i], input_tuple[1][i]))
        return list

    class Agent:
        def __init__(self, initial_pos, initial_vel):
            self.pos = initial_pos
            self.vel = initial_vel

        def update_agent(self, new_pos, new_vel):
            self.pos = new_pos
            self.vel = new_vel

        def reset_velocity(self):
            # print("reset velocity")
            self.vel = (0, 0)
