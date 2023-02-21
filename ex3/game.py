import numpy as np
from state import State
from display import Display
from state import State
import random


class Game:
    def __init__(self, racetrack: np.ndarray, visualize = False):
        self.racetrack = racetrack
        self.visualize = visualize

        # initialize Agent with starting position and velocity
        self.agent = self.Agent(random.choice(self.get_start_cells()), (0, 0))

        # initalize the visualizer
        if visualize:
            state = State(self.racetrack, self.agent.pos)
            self.display = Display(state)

    def play_user(self):
        """
        This function starts the user game.
        """
        not_finsihed = True

        while not_finsihed:
            input_str = input("Please input the change to velocity. format: \"<y> <x>\": ")
            input_list = input_str.split(" ")
            input_tuple = (int(input_list[0]),int(input_list[1]))
            self.step(input_tuple)
            if self.is_finished():
                not_finsihed = False
                print("You reached the finish line!")

    def is_finished(self):
        if self.agent.pos in self.get_end_cells():
            return True
        return False

    def step(self, game_input: tuple[int,int]):
        """
        TODO do

        :param game_input: This represents the input of the user/agent and indicates how the velocity should be changed
        :return: returns current state. # TODO finish comment
        """
        # TODO maybe introduce a limit to the velocity, like the article?
        # TODO is the car allowed to drive backwards?

        # create new velocity. If it is valid, set the agent velocity to the new velocity
        self.agent.vel = self.check_velocity(game_input)

        # create new position. If it is valid, set the agent position to the new position
        self.agent.pos = self.check_pos()

        if self.visualize:
            self.display.update_agent(self.agent.pos)

    def check_pos(self):
        """
        Checks if the position is still valid after applying the velocity. If it is valid the new position is
        returned, else the old one is returned.

        :return: Returns new position if it is valid, else it returns the old one
        """
        new_pos = (self.agent.pos[0] + self.agent.vel[0], self.agent.pos[1] - self.agent.vel[1]) # self.agent.pos[1] + self.agent.vel[1]

        # checking if it is out of bounds
        # car cant move out of the grid.
        if new_pos[0] >= self.racetrack.shape[0]:
            new_pos = (self.racetrack.shape[0]-1, new_pos[1])
        if new_pos[0] < 0:
            new_pos = (0, new_pos[1])
        if new_pos[1] >= self.racetrack.shape[1]:
            new_pos = (new_pos[0], self.racetrack.shape[1]-1)
        if new_pos[1] < 0:
            new_pos = (new_pos[0], 0)

        # checking if it is on an invalid cell
        if self.racetrack[new_pos[0]][new_pos[1]] == 0:
            self.agent.reset_velocity()
            return random.choice(self.get_start_cells())

        # if is has not returned yet, the position is valid
        return new_pos

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

        # checks if velocity is >= 0 and < 5
        if new_vel[0] > 4 or new_vel[0] < 0 or new_vel[1] > 4 or new_vel[1] < 0:
            print("Exceeded Velocity limits")
            return self.agent.vel

        return new_vel

    def get_state(self) -> State:
        """
        Returns the current state of the game

        :return: returns current state.
        """
        return State(self.racetrack, self.agent.pos)

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
            print("reset velocity")
            self.vel = (0, 0)
