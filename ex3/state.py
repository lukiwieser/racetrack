import numpy as np

class State:
    def __init__(self, racetrack: np.ndarray, agent_position: tuple[int,int]):
        self.racetrack = racetrack
        self.agent_position = agent_position

    def setAgent(self, new_pos: tuple[int,int]):
        self.agent_position = new_pos