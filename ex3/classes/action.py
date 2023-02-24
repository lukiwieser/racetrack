class Action:
    def __init__(self, x, y):
        self.x = x  # increase in x velocity
        self.y = y  # increase in y velocity

    def __eq__(self, other):
        if isinstance(other, Action):
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

    def __repr__(self):
        return f"Action({self.x},{self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
