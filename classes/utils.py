import argparse

import numpy as np

from classes.generator import Generator
from classes.racetrack_list import RacetrackList


def check_positive_int(value_str: str):
    try:
        value = int(value_str)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value_str} is not an integer")
    if value <= 0:
        raise argparse.ArgumentTypeError(f"{value_str} is not a positive integer")
    return value


def get_track(track_number: int | None, track_random_seed: int | None) -> np.ndarray:
    if track_number is not None:
        return RacetrackList.get_track(track_number)
    if track_random_seed is not None:
        g = Generator(random_state=track_random_seed)
        return g.generate_racetrack_safely(size=50, n_edges=4, kernel_size=7)
    raise ValueError("either track_number or track_random_seed must have a value")