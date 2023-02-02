from state import State
from vizualizer import Visualizer
import numpy as np
import time


map = np.ones(shape=(50,50))
map[:,4] = 0
map[:,5] = 0
map[49,4] = 2
map[49,5] = 2
map[0,4] = 3
map[0,5] = 3
print(map)

state = State(map, (7,4))
viz = Visualizer(state)

time.sleep(5)
# viz.updateAgent((7,1))