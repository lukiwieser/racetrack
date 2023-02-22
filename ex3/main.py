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

    # map 2
    map[:35, 19:29] = 1
    map[19:35, 19:44] = 1
    map[35:49, 35:44] = 1
    map[49, 35:44] = 3
    map[0, 19:29] = 2

    # map 1
    # map[:35, 19:29] = 1
    # map[19:35, 19:49] = 1
    # map[19:35, 49] = 3
    # map[0, 19:29] = 2

    g = Game(racetrack=map, visualize=True)

    while not g.is_finished():
        input_str = input("Please input the change to velocity. format: \"<y> <x>\": ")
        input_list = input_str.split(" ")
        action = Action(int(input_list[0]), int(input_list[1]))
        g.step(action)

    print("You reached the finish line!")

def train_ai():

    map = np.zeros(shape=(50, 50))

    # map 2
    map[:35, 19:29] = 1
    map[19:35, 19:44] = 1
    map[35:49, 35:44] = 1
    map[49, 35:44] = 3
    map[0, 19:29] = 2

    # # map 1
    # map[:35, 19:29] = 1
    # map[19:35, 19:49] = 1
    # map[19:35, 49] = 3
    # map[0, 19:29] = 2

    game = Game(racetrack=map, visualize=False)
    model = ModelRLMC()

    for i in range(0, 3000):
        episode: list[tuple[State, Action, int]] = []
        n_steps = 0
        while not game.is_finished() and n_steps < 1000:
            state = game.get_state()
            action = model.determine_action(state)
            reward = game.step(action)
            episode.append((state,action,reward))
            n_steps += 1
        if i % 500 == 0:
            print(str(n_steps) + " " + str(i))
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
        game.step(action)
        print(f"action: {action}, pos: {game.get_state().agent_position}, vel: {game.get_state().agent_velocity}")
        n_steps += 1
        time.sleep(1)




train_ai()
# play_user()