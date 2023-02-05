from functools import partial
from state import State
from vizualizer import Visualizer
import threading
import copy

class Display:
    def vis(self, state):
        vis = Visualizer(state)

    def __init__(self, state: State):
        self.state = copy.deepcopy(state)
        t = threading.Thread(target=partial(self.vis, self.state))
        t.start()

    def update_agent(self, new_pos: tuple[int,int]):
        self.state.setAgent(new_pos)
