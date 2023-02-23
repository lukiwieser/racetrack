from game import Game
import numpy as np
from model import ModelRLMC
from action import Action
from state import State
import racetrack_list as rlist
import time
from displayEpisode import DisplayEpisode

import random
random.seed(42)

def play_user():
    track = rlist.get_track1()
    g = Game(racetrack=track, visualize=True)

    while not g.is_finished():
        input_str = input("Please input the change to velocity. format: \"<y> <x>\": ")
        input_list = input_str.split(" ")
        action = Action(int(input_list[0]), int(input_list[1]))
        g.step(action)

    print("You reached the finish line!")

def train_ai():
    track = rlist.get_track1()
    game = Game(racetrack=track, visualize=False)
    model = ModelRLMC()

    start = time.time()
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
    end = time.time()
    print(f"train time: {end - start}")

    # play interactively
    #game = Game(racetrack=map, visualize=True)
    #n_steps = 0
    #while not game.is_finished() and n_steps < 1000:
    #    print(f"ai plays step {n_steps}")
    #    state = game.get_state()
    #    action = model.determine_action(state)
    #    game.step(action)
    #    print(f"action: {action}, pos: {game.get_state().agent_position}, vel: {game.get_state().agent_velocity}")
    #    n_steps += 1
    #    time.sleep(0.5)

    displayEpisode = DisplayEpisode()
    for _ in range(0,3):
        game = Game(racetrack=map, visualize=False)
        n_steps = 0
        episode: list[tuple[State, Action, int]] = []
        while not game.is_finished() and n_steps < 1000:
            state = game.get_state()
            action = model.determine_action(state)
            reward = game.step(action)
            episode.append((state,action,reward))
            n_steps += 1
        displayEpisode.displayEpisode(map, episode)


train_ai()
# play_user()