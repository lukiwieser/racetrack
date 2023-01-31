import numpy as np


class Generator:
    """
    Generator for generating random racetracks.

    :param random_state: Used for generating the randomness of the racetrack. Pass an int for reproducible output across multiple function calls
    """

    def __init__(self, random_state: int):
        self.random_state = random_state

    def generate_racetrack(self) -> np.ndarray:
        """
        Generates a random racetrack.

        :return:  Returns a 2d numpy array, where each element represents a cell of the racetrack. The first dimension is the row, the second is the colum.
        """
        return None
