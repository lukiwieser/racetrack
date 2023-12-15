import numpy as np


class RacetrackList(object):
    """
    Predefined list of racetracks.
    """
    __tracks: list[np.ndarray] = []

    @classmethod
    def _init_tracks(cls):
        cls.__tracks = []
        cls.__tracks.append(cls.__get_track_0())
        cls.__tracks.append(cls.__get_track_1())
        cls.__tracks.append(cls.__get_track_2())

    @classmethod
    def get_track(cls, track_number: int) -> np.ndarray:
        return cls.__tracks[track_number]

    @classmethod
    def get_tracks_count(cls) -> int:
        return len(cls.__tracks)

    @classmethod
    def __get_track_0(cls) -> np.ndarray:
        track = np.zeros(shape=(50, 50))
        track[:35, 19:29] = 1
        track[19:35, 19:49] = 1
        track[19:35, 49] = 3
        track[0, 19:29] = 2
        return track

    @classmethod
    def __get_track_1(cls) -> np.ndarray:
        track = np.zeros(shape=(50, 50))
        track[:35, 19:29] = 1
        track[19:35, 19:44] = 1
        track[35:49, 35:44] = 1
        track[49, 35:44] = 3
        track[0, 19:29] = 2
        return track

    @classmethod
    def __get_track_2(cls) -> np.ndarray:
        track = np.zeros(shape=(50, 50))
        track[:35, 19:29] = 1
        track[19:35, 0:19] = 1
        track[19:35, 0] = 3
        track[0, 19:29] = 2
        return track


RacetrackList._init_tracks()
