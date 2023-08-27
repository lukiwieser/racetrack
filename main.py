import argparse
import time

import numpy as np

from classes.action import Action
from classes.episode_visualizer import EpisodeVisualizer
from classes.game import Game
from classes.interactive_visualizer import InteractiveVisualizer
from classes.model import ModelRLMC
from classes.state import State
from classes.racetrack_list import RacetrackList
from classes.utils import check_positive_int, get_track


def play_user(track: np.ndarray) -> None:
    """
    Let the user play a game on a racetrack

    :param track: The racetrack for the game
    """

    game = Game(racetrack=track, random_state=42)
    visualizer = InteractiveVisualizer(game.get_state_with_racetrack(), "racetrack")

    print("Playing as user...")
    while not game.is_finished():
        print(f"* {game.get_state()}")
        input_str = input("* Please input the change to velocity. format: \"<y> <x>\": ")
        input_list = input_str.split(" ")
        action = Action(int(input_list[0]), int(input_list[1]))
        game.step(action)
        visualizer.update_agent(game.get_state().agent_position)

    print("* You reached the finish line!")


def play_ai(track: np.ndarray, episodes_to_train: int, playstyle_interactive: bool) -> None:
    """
    Train an AI on a racetrack, and then watch it play.

    :param track: The racetrack for the game
    :param episodes_to_train: How many episodes to train the model
    :param playstyle_interactive: If the game that AI plays should be shown life (aka interactively), or if the whole game should be shown in one static image (not interactively)
    """

    model = ModelRLMC(random_state=42)
    game = Game(racetrack=track, random_state=42)

    # Train Model
    print("Training model...")
    print("* <n_steps> <n_episode>")
    start = time.time()
    for i in range(0, episodes_to_train):
        episode: list[tuple[State, Action, int]] = []
        while not game.is_finished() and game.get_n_steps() < 1000:
            state = game.get_state()
            action = model.determine_epsilon_action(state, 0.1)
            reward = game.noisy_step(action)
            episode.append((state, action, reward))
        if i % 500 == 0:
            print(f"* {game.get_n_steps()} {i}")
        model.learn(episode)
        game.reset()
    end = time.time()
    print(f"* train time: {end - start : 2.4f}s")

    # Evaluate Model
    print("Evaluating trained model...")
    if playstyle_interactive:
        visualizer = InteractiveVisualizer(game.get_state_with_racetrack(), "racetrack")
        while not game.is_finished() and game.get_n_steps() < 1000:
            state = game.get_state()
            action = model.determine_best_action(state)
            game.step(action)
            visualizer.update_agent(game.get_state().agent_position)
            print(f"* ai plays step {game.get_n_steps()} [action: {action}, pos: {game.get_state().agent_position}, vel: {game.get_state().agent_velocity}]")
            time.sleep(0.5)
        print("* ai reached the finish line!")
    else:
        print("* plotting 3 games")
        visualizer = EpisodeVisualizer()
        for i in range(0, 3):
            episode: list[tuple[State, Action, int]] = []
            while not game.is_finished() and game.get_n_steps() < 1000:
                state = game.get_state()
                action = model.determine_best_action(state)
                reward = game.step(action)
                episode.append((state, action, reward))
            visualizer.visualize_episode(track, episode, f"racetrack | testrun {i+1}")
            game.reset()


def main() -> None:
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