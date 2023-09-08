import argparse
import copy
import time

import numpy as np

from classes.action import Action
from classes.episode_visualizer import EpisodeVisualizer
from classes.game import Game
from classes.interactive_visualizer import InteractiveVisualizer
from classes.model import ModelRLMC
from classes.racetrack_list import RacetrackList
from classes.state import State
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


def play_single_game(game: Game, model: ModelRLMC) -> list[tuple[State, Action, int]]:
    episode: list[tuple[State, Action, int]] = []
    while not game.is_finished() and game.get_n_steps() < 1000:
        state = game.get_state()
        action = model.determine_best_action(state)
        reward = game.step(action)
        episode.append((state, action, reward))
    return episode


def play_ai(track: np.ndarray, episodes_to_train: int, preliminary_results: int | None, testruns: int,
            playstyle_interactive: bool) -> None:
    """
    Train an AI on a racetrack, and then watch it play.

    :param track: The racetrack for the game
    :param episodes_to_train: How many episodes to train the model
    :param playstyle_interactive: If the game that AI plays should be shown life (aka interactively), or if the whole game should be shown in one static image (not interactively)
    :param preliminary_results: After how many episodes to show preliminary results (aka do a test run). If `None`, then no preliminary results will be shown.
    """

    if not playstyle_interactive:
        preliminary_results = None

    model = ModelRLMC(random_state=42)
    game = Game(racetrack=track, random_state=42)
    visualizer = EpisodeVisualizer()

    # Train Model
    print("Training model...")
    if preliminary_results is not None:
        print("* <n_episode> <n_steps> ")
    else:
        print("* <n_episode> ")
    start = time.time()
    for i in range(1, episodes_to_train + 1):
        # play one episode & train the model on this episode
        episode: list[tuple[State, Action, int]] = []
        while not game.is_finished() and game.get_n_steps() < 1000:
            state = game.get_state()
            action = model.determine_epsilon_action(state, 0.1)
            reward = game.noisy_step(action)
            episode.append((state, action, reward))
        model.learn(episode)
        game.reset()
        # show preliminary results, if specified
        if preliminary_results is not None:
            if i % preliminary_results == 0 or i == 1:
                test_game = Game(racetrack=track, random_state=43)
                test_episode = play_single_game(test_game, copy.deepcopy(model))
                visualizer.visualize_episode(track, test_episode,
                                             f"racetrack | training: n_episode={i}, n_steps={test_game.get_n_steps()}")
                print(f"* {i} {test_game.get_n_steps()}")
        elif i % 500 == 0:
            print(f"* {i}")
    end = time.time()
    print(f"* train time: {end - start : 2.4f}s")

    # Evaluate Model
    game = Game(racetrack=track, random_state=43)
    print("Evaluating trained model...")
    if playstyle_interactive:
        visualizer = InteractiveVisualizer(game.get_state_with_racetrack(), "racetrack")
        while not game.is_finished() and game.get_n_steps() < 1000:
            state = game.get_state()
            action = model.determine_best_action(state)
            game.step(action)
            visualizer.update_agent(game.get_state().agent_position)
            print(
                f"* ai plays step {game.get_n_steps()} [action: {action}, pos: {game.get_state().agent_position}, vel: {game.get_state().agent_velocity}]")
            time.sleep(0.5)
        print("* ai reached the finish line!")
    else:
        print(f"* plotting {testruns} games")
        visualizer = EpisodeVisualizer()
        for i in range(0, testruns):
            episode: list[tuple[State, Action, int]] = []
            while not game.is_finished() and game.get_n_steps() < 1000:
                state = game.get_state()
                action = model.determine_best_action(state)
                reward = game.step(action)
                episode.append((state, action, reward))
            visualizer.visualize_episode(track, episode, f"racetrack | testrun {i + 1}, n_steps={game.get_n_steps()}")
            game.reset()


def main() -> None:
    # define arguments
    parser = argparse.ArgumentParser(prog="racetrack", description="Train an AI to drive on a simple racetrack, by using reinforcement learning with monte carlo")
    parser.add_argument('-p', '--playstyle', help="if the AI should play the game live (ai_interactive), or the game of the AI should be shown as static image (ai_static), or the user can play (user)", choices=["user", "ai_interactive", "ai_static"], default="ai_static")
    parser.add_argument('-e', '--episodes-to-train', help="how many episodes to train the model", type=check_positive_int, default=3000)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-tr', '--track-random', help="generate a random racetrack with specified seed", type=check_positive_int, metavar='SEED')
    group.add_argument('-tn', '--track-number', help="select a predefined racetrack, where the number represents the number of the map", type=int, choices=range(0, RacetrackList.get_tracks_count()))
    parser.add_argument('-pr', '--preliminary-results', help="after how many episodes to show a preliminary result during training (only for ai_static)", type=check_positive_int)
    parser.add_argument('-fr', '--final-results', help="how many final games to show after training (only for ai_static)", type=check_positive_int)

    # parse arguments
    args = parser.parse_args()
    playstyle = args.playstyle
    episodes_to_train = args.episodes_to_train
    preliminary_results = args.preliminary_results
    final_results = args.final_results
    track_random_seed = args.track_random
    track_number = args.track_number
    if track_number is None and track_random_seed is None:
        track_number = 0  # set default
    if final_results is None and playstyle == "ai_static":
        final_results = 3  # set default

    # print start configuration
    print("Starting new game with:")
    print(f"* playstyle = {playstyle}")
    if track_number is not None:
        print(f"* track = track {track_number}")
    else:
        print(f"* track = random with seed {track_random_seed}")
    print(f"* episodes to train = {episodes_to_train}")
    if playstyle == "ai_static":
        if preliminary_results is None:
            print(f"* preliminary results during training = none")
        else:
            print(f"* preliminary results during training = all {preliminary_results} episodes")
    elif preliminary_results is not None:
        print(f"* note: parameter 'preliminary_results' is ignored since playstyle is not 'ai_static'")
    if playstyle == "ai_static":
        print(f"* final results after training = {final_results} games")
    elif final_results is not None:
        print(f"* note: parameter 'final_results' is ignored since playstyle is not 'ai_static'")

    # get track & play
    track = get_track(track_number, track_random_seed)
    match playstyle:
        case "user":
            play_user(track)
        case "ai_interactive":
            play_ai(track, episodes_to_train, preliminary_results, final_results, playstyle_interactive=True)
        case "ai_static":
            play_ai(track, episodes_to_train, preliminary_results, final_results, playstyle_interactive=False)


if __name__ == "__main__":
    main()
