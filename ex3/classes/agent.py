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