import copy
import threading
from functools import partial
from tkinter import *


class EpisodeVisualizer:
    """
    Visualizing one game as a static image.
    The game is given by a single episode.
    """

    def visualize_episode(self, map, episode, title):
        t = threading.Thread(target=partial(self._run_in_thread, map, episode, title))
        t.start()

    def _run_in_thread(self, map, episode, title):
        vis = EpisodeVisualizerIntern(map, episode, title)

class EpisodeVisualizerIntern:
    def __init__(self, map, episode, title, boardsize=600):
        self.map = copy.deepcopy(map)
        self.episode = copy.deepcopy(episode)

        # initiate the gameboard
        self.init_board(boardsize, title)

    def init_board(self, boardsize, title):
        """
        Creates the tkinter window and initializes it with the correct state.

        :param boardsize: The size of the wanted board.
        """
        self.window = Tk()
        self.window.title(title)
        self.canvas = Canvas(self.window, width=boardsize, height=boardsize)
        self.canvas.pack()

        # create grid of rectangles and safe it
        self.board = self.create_board(copy.deepcopy(self.map), boardsize)

        # draw epsiode
        self.draw_episode()

        # start blocking main loop
        self.window.mainloop()

    def draw_episode(self):
        for t in self.episode:
            pos = t[0].agent_position
            self.change_color(self.board[pos[0]][pos[1]])

    def change_color(self, item):
        """
        Changes the color of a specific rectangle in the grid.

        :param item: The rectangle, which color should be changed.
        """
        self.canvas.itemconfig(int(item), fill="red")

    def create_board(self, input_array, boardsize):
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

    def get_color(self, num: int):
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
