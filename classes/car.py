class Car:
    def __init__(self, initial_pos: tuple[int, int], initial_vel: tuple[int, int]):
        self.pos = initial_pos
        self.vel = initial_vel

    def reset_velocity(self):
        self.vel = (0, 0)
