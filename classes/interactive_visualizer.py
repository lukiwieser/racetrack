import copy
import threading
from functools import partial
from tkinter import *
from typing import Any

import numpy as np

from .state_with_racetrack import StateWithRacetrack


class InteractiveVisualizer:
    """
    Visualizing a game as a dynamic image.
    If the state of the game changes the visualization also changes dynamically.
    """

    def __init__(self, state: StateWithRacetrack, title: str):
        self.state = copy.deepcopy(state)
        t = threading.Thread(target=partial(self._run_in_thread, self.state, title))
        t.start()

    def update_agent(self, new_pos: tuple[int, int]) -> None:
        self.state.agent_position = new_pos

    def _run_in_thread(self, state: StateWithRacetrack, title: str) -> None:
        InteractiveVisualizerIntern(state, title)


class InteractiveVisualizerIntern:
    def __init__(self, state: StateWithRacetrack, title: str, boardsize: int = 600):
        self.state = state
        self.old_state = copy.deepcopy(state)
        self.back_up_map = copy.deepcopy(state.racetrack)

        # initiate the gameboard
        self.init_board(boardsize, title)

        # start the event loop that checks for position changes
        self.window.after(0, self.check_for_state_change)

        # start blocking main loop
        self.window.mainloop()

    def init_board(self, boardsize: int, title: str) -> None:
        """
        Creates the tkinter window and initializes it with the correct state.

        :param boardsize: The size of the wanted board.
        """
        self.window = Tk()
        self.window.title(title)
        self.canvas = Canvas(self.window, width=boardsize, height=boardsize)
        self.canvas.pack()

        # create grid of rectangles and safe it
        self.board = self.create_board(self.state.racetrack, boardsize)

        # set initial position of agent
        self.change_color(self.board[self.state.agent_position[0]][self.state.agent_position[1]], "red")

    def create_board(self, input_array: np.ndarray, boardsize: int) -> np.ndarray:
        """
        Converts the initial ndarray-2d array into a grid of rectangles.

        Assumption: the input array has the structure NxN

        :param input_array: Initial racecourse
        :param boardsize: size of the displayed board. This is needed so the rectangles have the proper size.
        """
        for i in range(input_array.shape[0]):
            for j in range(input_array.shape[1]):
                cell_size = boardsize / input_array.shape[0]
                color = self.get_color(input_array[i][j])
                x1 = j * cell_size
                y1 = (input_array.shape[0] - 1) * cell_size - i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                input_array[i][j] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        return input_array

    def get_color(self, num: int) -> str:
        """
        Returns color corresponding to the cell type.

        :param num: integer that represents the cell type.
        """
        if num == 0:
            return "white"
        elif num == 1:
            return "black"
        elif num == 2:
            return "yellow"
        else:
            return "green"

    def change_color(self, item: Any, color: str) -> None:
        """
        Changes the color of a specific rectangle in the grid.

        :param item: The rectangle, which color should be changed.
        """
        self.canvas.itemconfig(int(item), fill=color)

    def update_agent(self) -> None:
        """
        Updates the rectangles with the correct colors
        """

        # reset color of old position
        old_color = self.get_color(self.back_up_map[self.old_state.agent_position[0]][self.old_state.agent_position[1]])
        self.change_color(self.board[self.old_state.agent_position[0]][self.old_state.agent_position[1]], old_color)

        # color new position correct
        self.change_color(self.board[self.state.agent_position[0]][self.state.agent_position[1]], "red")

    def check_for_state_change(self) -> None:
        """
        Checks if the position of the car changed and adjusts the coloring of the rectangles if it is necessary.
        After that it puts itself in the event loop again.
        """
        if self.state.agent_position == self.old_state.agent_position:
            pass
        else:
            self.update_agent()
            self.old_state.agent_position = copy.deepcopy(self.state.agent_position)
        self.window.update()
        self.window.after(0, self.check_for_state_change)
