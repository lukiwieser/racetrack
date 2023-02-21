import numpy as np


class State:
    def __init__(self, agent_position: tuple[int, int], agent_velocity: tuple[int, int]):
        # self.racetrack = racetrack
        self.agent_position = agent_position
        self.agent_velocity = agent_velocity

    def setAgent(self, new_pos: tuple[int, int], new_vel: tuple[int, int]):
        self.agent_position = new_pos
        self.agent_velocity = new_vel

    def __eq__(self, other):
        if isinstance(other, State):
            return self.agent_position == other.agent_position and self.agent_velocity == other.agent_velocity
        return NotImplemented

    def __repr__(self):
        return f"State(pos:{self.agent_position}, vel:{self.agent_velocity})"

    def __hash__(self):
        return hash((self.agent_position, self.agent_velocity))

    def __lt__(self, other):
        if self.agent_position < other.agent_position:
            return True
        if self.agent_position > other.agent_position:
            return False
        if self.agent_velocity < other.agent_velocity:
            return True
        return False
