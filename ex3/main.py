import numpy as np
import racetrack_list as rlist
import time
import argparse
from game import Game
from model import ModelRLMC
from action import Action
from state import State
from displayEpisode import DisplayEpisode
from generator import Generator


def play_user():
    # track = rlist.get_track1()
    g = Generator(random_state=42)
    track = g.generate_racetrack_safely(size=50, n_edges=4, kernel_size=7)
    track = g.generate_racetrack_safely(size=50, n_edges=4, kernel_size=7)[::-1]
    g = Game(racetrack=track, visualize=True, random_state=42)

    while not g.is_finished():
        print(g.get_state())
        input_str = input("Please input the change to velocity. format: \"<y> <x>\": ")
        input_list = input_str.split(" ")
        action = Action(int(input_list[0]), int(input_list[1]))
        g.step(action)

    print("You reached the finish line!")


def play_ai(playstyle_interactive = False):
    # track1 = rlist.get_track2()
    model = ModelRLMC(random_state=42)
    g = Generator(random_state=42)
    track = g.generate_racetrack_safely(size=50, n_edges=4, kernel_size=7)

    # Train Model
    game = Game(racetrack=track, visualize=False, random_state=42)
    start = time.time()
    for i in range(0, 10000):
        episode: list[tuple[State, Action, int]] = []
        n_steps = 0
        while not game.is_finished() and n_steps < 1000:
            state = game.get_state()
            action = model.determine_epsilon_action(state)
            reward = game.noisy_step(action)
            episode.append((state, action, reward))
            n_steps += 1
        if i % 500 == 0:
            print(str(n_steps) + " " + str(i))
        model.learn(episode)
        game.reset()
    end = time.time()
    print(f"train time: {end - start}")

    # Evaluate Model
    # We use a different seed so that the game behaves differently
    if playstyle_interactive:
        game = Game(racetrack=track, visualize=True, random_state=43)
        n_steps = 0
        while not game.is_finished() and n_steps < 1000:
            print(f"ai plays step {n_steps}")
            state = game.get_state()
            action = model.determine_best_action(state)
            game.step(action)
            print(f"action: {action}, pos: {game.get_state().agent_position}, vel: {game.get_state().agent_velocity}")
            n_steps += 1
            time.sleep(0.5)
    else:
        print("plotting 3 games")
        displayEpisode = DisplayEpisode()
        game = Game(racetrack=track, visualize=False, random_state=43)
        for _ in range(0, 3):
            game.reset()
            n_steps = 0
            episode: list[tuple[State, Action, int]] = []
            while not game.is_finished() and n_steps < 1000:
                state = game.get_state()
                action = model.determine_best_action(state)
                reward = game.step(action)
                episode.append((state, action, reward))
                n_steps += 1
            displayEpisode.displayEpisode(track, episode)


def main():
    parser = argparse.ArgumentParser("machine learning ex3")
    parser.add_argument('-m', '--mode', help="c", choices=["user","ai_interactive","ai_static"], default="ai_static")
    args = parser.parse_args()

    mode = args.mode
    print(f"{mode = }")
    match mode:
        case "user": play_user()
        case "ai_interactive": play_ai(playstyle_interactive=True)
        case "ai_static": play_ai(playstyle_interactive=False)


if __name__ == "__main__":
    main()
