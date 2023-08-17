import argparse
import time

import numpy as np

from classes.action import Action
from classes.episode_visualizer import EpisodeVisualizer
from classes.game import Game
from classes.generator import Generator
from classes.model import ModelRLMC
from classes.state import State
from classes.racetrack_list import RacetrackList


def play_user(track: np.ndarray) -> None:
    """
    Let the user play a game on a racetrack

    :param track: the racetrack for the game
    """

    game = Game(racetrack=track, visualize=True, random_state=42)

    print("Playing as user...")
    while not game.is_finished():
        print(f"* {game.get_state()}")
        input_str = input("* Please input the change to velocity. format: \"<y> <x>\": ")
        input_list = input_str.split(" ")
        action = Action(int(input_list[0]), int(input_list[1]))
        game.step(action)

    print("* You reached the finish line!")


def play_ai(track: np.ndarray, episodes_to_train: int, playstyle_interactive: bool) -> None:
    """
    Train an AI on a racetrack, and then watch it play.

    :param track: the racetrack for the game
    :param playstyle_interactive: if the game that AI plays should be shown life (aka interactively), or if the whole game should be shown in one static image (not interactively)
    """

    model = ModelRLMC(random_state=42)

    # Train Model
    print("Training model...")
    print("* <n_steps> <n_episode>")
    game = Game(racetrack=track, visualize=False, random_state=42)
    start = time.time()
    for i in range(0, episodes_to_train):
        episode: list[tuple[State, Action, int]] = []
        n_steps = 0
        while not game.is_finished() and n_steps < 1000:
            state = game.get_state()
            action = model.determine_epsilon_action(state, 0.1)
            reward = game.noisy_step(action)
            episode.append((state, action, reward))
            n_steps += 1
        if i % 500 == 0:
            print(f"* {n_steps} {i}")
        model.learn(episode)
        game.reset()
    end = time.time()
    print(f"* train time: {end - start : 2.4f}s")

    # Evaluate Model
    # We use a different seed so that the game behaves differently for evaluation
    print("Evaluating trained model...")
    if playstyle_interactive:
        game = Game(racetrack=track, visualize=True, random_state=43)
        n_steps = 0
        while not game.is_finished() and n_steps < 1000:
            state = game.get_state()
            action = model.determine_best_action(state)
            game.step(action)
            print(f"* ai plays step {n_steps} [action: {action}, pos: {game.get_state().agent_position}, vel: {game.get_state().agent_velocity}]")
            n_steps += 1
            time.sleep(0.5)
    else:
        print("* plotting 3 games")
        visualizer = EpisodeVisualizer()
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
            visualizer.visualize_episode(track, episode)


def check_positive_int(value_str: str):
    try:
        value = int(value_str)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value_str} is not an integer")
    if value <= 0:
        raise argparse.ArgumentTypeError(f"{value_str} is not a positive integer")
    return value


def get_track(track_number: int | None, track_random_seed: int | None) -> np.ndarray:
    if track_number is not None:
        return RacetrackList.get_track(track_number)
    if track_random_seed is not None:
        g = Generator(random_state=track_random_seed)
        return g.generate_racetrack_safely(size=50, n_edges=4, kernel_size=7)
    raise ValueError("either track_number or track_random_seed must have a value")


def main():
    # define arguments
    parser = argparse.ArgumentParser(prog="racetrack", description="Train an AI to drive on a simple racetrack, by using reinforcement learning with monte carlo")
    parser.add_argument('-p', '--playstyle', help="if the AI should play the game live (ai_interactive), or the game of the AI should be shown as static image (ai_static), or the user can play (user)", choices=["user", "ai_interactive", "ai_static"], default="ai_static")
    parser.add_argument('-e', '--episodes-to-train', help="how many episodes to train the model", type=check_positive_int, default=3000)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-tr', '--track-random', help="generate a random racetrack with specified seed", type=check_positive_int, metavar='SEED')
    group.add_argument('-tn', '--track-number', help="select a predefined racetrack, where the number represents the number of the map", type=int, choices=range(0, RacetrackList.get_tracks_count()))

    # parse arguments
    args = parser.parse_args()
    episodes_to_train = args.episodes_to_train
    playstyle = args.playstyle
    track_random_seed = args.track_random
    track_number = args.track_number
    if track_number is None and track_random_seed is None:
        track_number = 0  # set default params if both track-options are none

    # print start configuration
    print("Starting new game with:")
    print(f"* {playstyle = }")
    if track_number is not None:
        print(f"* track = track {track_number}")
    if track_random_seed is not None:
        print(f"* track = random with seed {track_random_seed}")
    print(f"* episodes to train = {episodes_to_train}")

    # get track & play
    track = get_track(track_number, track_random_seed)
    match playstyle:
        case "user":
            play_user(track)
        case "ai_interactive":
            play_ai(track, episodes_to_train, playstyle_interactive=True)
        case "ai_static":
            play_ai(track, episodes_to_train, playstyle_interactive=False)


if __name__ == "__main__":
    main()
