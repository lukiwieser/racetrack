from state import State
from action import Action
from collections import defaultdict
from statistics import mean


class ModelRLMC:
    def __init__(self):
        self.gamma = 0.9
        self.q: dict[tuple[State, Action], int] = {}  # expected return for given state-action-pair
        self.returns: defaultdict[tuple[State, Action], list[int]] = defaultdict(list)

    def determine_action(self, state: State) -> Action:
        action_space = [
            Action(-1,-1),
            Action( 0,-1),
            Action( 1,-1),
            Action(-1, 0),
            Action( 0, 0),
            Action( 1, 0),
            Action(-1, 1),
            Action( 0, 1),
            Action( 1, 1)
        ]
        expected_rewards = []
        for action in action_space:
            expected_rewards.append(self.q[(state, action)])

        pass

    def learn(self, episode: list[tuple[State, Action, int]]):
        episode_reversed = list(reversed(episode))
        g = 0
        for i, (state, action, reward) in enumerate(episode_reversed):
            g = self.gamma * g + reward
            print(f"{i}: {state},{action},{reward} {g}")

            is_first_state_action_pair = True
            for _, (state_pre, action_pre, reward_pre) in enumerate(episode_reversed[i + 1::]):
                if state == state_pre and action == action_pre:
                    is_first_state_action_pair = False

            if is_first_state_action_pair:
                self.returns[(state, action)].append(g)
                self.q[(state, action)] = mean(self.returns[(state, action)])