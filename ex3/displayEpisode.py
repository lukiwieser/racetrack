from functools import partial
from state_with_racetrack import StateWithRacetrack
from episodeVisualizer import EpisodeVisualizer
import threading
import copy

class DisplayEpisode:
    def __display(self, map, episode):
        vis = EpisodeVisualizer(map, episode)

    def displayEpisode(self, map, episode):
        t = threading.Thread(target=partial(self.__display, map, episode))
        t.start()

