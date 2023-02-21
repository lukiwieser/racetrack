from functools import partial
from state_with_racetrack import StateWithRacetrack
from vizualizer import Visualizer
import threading
import copy

class Display:
    def __vis(self, state):
        vis = Visualizer(state)

    def __init__(self, state: StateWithRacetrack):
        self.state = copy.deepcopy(state)
        t = threading.Thread(target=partial(self.__vis, self.state))
        t.start()

    def update_agent(self, new_pos: tuple[int,int]):
        self.state.agent_position = new_pos
