import numpy as np


def get_track1() -> np.ndarray:
    track = np.zeros(shape=(50, 50))
    track[:35, 19:29] = 1
    track[19:35, 19:49] = 1
    track[19:35, 49] = 3
    track[0, 19:29] = 2
    return track


def get_track2() -> np.ndarray:
    track = np.zeros(shape=(50, 50))
    track[:35, 19:29] = 1
    track[19:35, 19:44] = 1
    track[35:49, 35:44] = 1
    track[49, 35:44] = 3
    track[0, 19:29] = 2
    return track
