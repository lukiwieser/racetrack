class Agent:
    def __init__(self, initial_pos: tuple[int, int], initial_vel: tuple[int, int]):
        self.pos = initial_pos
        self.vel = initial_vel

    def update_agent(self, new_pos: tuple[int, int], new_vel: tuple[int, int]):
        self.pos = new_pos
        self.vel = new_vel

    def reset_velocity(self):
        self.vel = (0, 0)
