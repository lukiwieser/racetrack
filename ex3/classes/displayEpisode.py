import threading
from functools import partial

from .episodeVisualizer import EpisodeVisualizer


class DisplayEpisode:
    def __display(self, map, episode):
        vis = EpisodeVisualizer(map, episode)

    def displayEpisode(self, map, episode):
        t = threading.Thread(target=partial(self.__display, map, episode))
        t.start()
