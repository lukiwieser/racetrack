from functools import partial

from state import State
from vizualizer import Visualizer
from game import Game
import threading
import numpy as np
import time


def please(state):
    vis = Visualizer(state)


map = np.ones(shape=(50, 50))
map[:, 4] = 0
map[:, 5] = 0
map[49, 4] = 2
map[49, 5] = 2
map[0, 4] = 3
map[0, 5] = 3
print(map)

# game = Game(map)
# game.play_user()

# print("hallo")

state = State(map, (7, 4))



t = threading.Thread(target=partial(please, state))
t.start()

print("hallo")
time.sleep(5)
state.setAgent((0, 0))
time.sleep(5)
state.setAgent((1, 1))
print("hallo")
