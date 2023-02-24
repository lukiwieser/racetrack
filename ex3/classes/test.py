from model import ModelRLMC
from state import State
from action import Action
import random


random.random()

from generator import Generator

g = Generator(random_state=None)
g.generate_racetrack(size=500, n_edges=2, kernel_size=70)




def asdf2():
    m = ModelRLMC()

    s = State((0, 1), (0, 1))
    a = m.determine_action(s)
    print(a)

def asdf():
    m = ModelRLMC()

    episode1 = [
        (State((0, 0), (0, 0)), Action(0, 1), -1),
        (State((0, 1), (0, 1)), Action(0, 0), -2),
        (State((0, 2), (0, 1)), Action(0, 0), -3),
        (State((0, 3), (0, 1)), Action(0, 0), -4),
        (State((0, 4), (0, 1)), Action(0, 0), -5),
        (State((0, 0), (0, 1)), Action(0, 0), -6),
    ]
    episode2 = [
        (State((0, 0), (0, 0)), Action(0, 1), -1),
        (State((0, 1), (0, 1)), Action(0, 1), -2),
        (State((0, 3), (0, 2)), Action(0, 0), -3),
        (State((0, 5), (0, 2)), Action(0, 0), -4),
        (State((0, 7), (0, 2)), Action(0, 0), -5),
    ]
    episode3 = [
        (State((0, 0), (0, 0)), Action(1, 0), -1),
        (State((1, 0), (1, 0)), Action(1, 0), -2),
        (State((2, 0), (2, 0)), Action(0, 0), -3),
        (State((4, 0), (2, 0)), Action(0, 0), -4),
        (State((6, 0), (2, 0)), Action(0, 0), -5),
    ]

    m.learn(episode1)
    m.learn(episode2)
    m.learn(episode3)

    print("m.q")

    for k, v in sorted(m.q.items()):
        print(f"{k} {v}")
