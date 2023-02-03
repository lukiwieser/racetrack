from state import State
from tkinter import *
import time

class Visualizer:
    def __init__(self, state: State, boardsize=600):
        self.state = state
        self.old_state = state
        self.init_board(boardsize)
        # self.window.after(2000, self.check_for_state_change())
        # self.check_for_state_change()
        self.window.mainloop()
        # self.window.update()

    def init_board(self, boardsize):
        """
        Creates the tkinter window and initializes it with the correct state.

        :param boardsize: The size of the wanted board.
        """
        self.window = Tk()
        self.canvas = Canvas(self.window, width=boardsize, height=boardsize)
        self.canvas.pack()

        # create grid of rectangles and safe it
        self.board = self.create_board(self.state.racetrack, boardsize)

        # set initial position of agent
        self.change_color(self.board[self.state.agent_position[0]][self.state.agent_position[1]], "red")

    def create_board(self, input_array, boardsize):
        """
        Converts the initial ndarray-2d array into a grid of rectangles.

        :param input_array: Initial racecourse
        :param boardsize: size of the displayed board. This is needed so the rectangles have the proper size.
        """
        for i in range(input_array.shape[0]):
            for j in range(input_array.shape[1]):
                cell_size = boardsize / input_array.shape[0]
                color = self.get_color(input_array[i][j])
                x1 = j * cell_size
                y1 = i * cell_size
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
            return "black"
        elif num == 1:
            return "white"
        elif num == 2:
            return "yellow"
        else:
            return "green"

    def change_color(self, item, color):
        """
        Changes the color of a specific rectangle in the grid.

        :param item: The rectangle, which color should be changed.
        """
        self.canvas.itemconfig(int(item), fill=color)

    def updateAgent(self, pos: tuple[int,int]):

        # reset color of old posiiton
        self.change_color(self.board[self.state.agent_position[0]][self.state.agent_position[1]], "black")

        # set new position of agent
        self.state.agent_position = pos

        # color new position correct
        self.change_color(self.board[self.state.agent_position[0]][self.state.agent_position[1]], "red")

    def check_for_state_change(self):
        g = input("why: ")
        # time.sleep(1)
        # if self.state.agent_position == self.old_state.agent_position:
        #     pass
        # else:
        #     self.updateAgent(self.state.agent_position)
        #     self.old_state.agent_position = self.state.agent_position
        self.window.update()
        self.window.after(2000, self.check_for_state_change())


