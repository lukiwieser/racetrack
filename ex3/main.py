from game import Game
import numpy as np
from model import ModelRLMC
from action import Action
from state import State
import time

import random
#random.seed(42)

def play_user():
    map = np.zeros(shape=(50, 50))
    map[:, 4] = 1
    map[:, 5] = 1
    map[49, 4] = 3
    map[49, 5] = 3
    map[0, 4] = 2
    map[0, 5] = 2

    g = Game(racetrack=map, visualize=True)

    while not g.is_finished():
        input_str = input("Please input the change to velocity. format: \"<y> <x>\": ")
        input_list = input_str.split(" ")
        action = Action(int(input_list[0]), int(input_list[1]))
        g.step(action)

    print("You reached the finish line!")

def train_ai():
    map = np.zeros(shape=(50, 50))
    map[:, 4] = 1
    map[:, 5] = 1
    map[49, 4] = 3
    map[49, 5] = 3
    map[0, 4] = 2
    map[0, 5] = 2

    game = Game(racetrack=map, visualize=False)
    model = ModelRLMC()

    for _ in range(0, 100):
        episode: list[tuple[State, Action, int]] = []
        n_steps = 0
        while not game.is_finished() and n_steps < 1000:
            state = game.get_state()
            action = model.determine_action(state)
            reward = game.step(action)
            episode.append((state,action,reward))
            n_steps += 1
        model.learn(episode)
        game.reset()

    #for k, v in sorted(model.q.items()):
    #    print(f"{k} {v}")

    # play
    game = Game(racetrack=map, visualize=True)
    n_steps = 0
    while not game.is_finished() and n_steps < 1000:
        print(f"ai plays step {n_steps}")
        state = game.get_state()
        action = model.determine_action(state)
        print(f"action: {action}")
        game.step(action)
        n_steps += 1
        time.sleep(2)




train_ai()
