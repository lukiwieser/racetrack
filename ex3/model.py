from state import State
from action import Action
from collections import defaultdict
import numpy as np
import random


class ModelRLMC:
    def __init__(self):
        self.gamma = 0.9
        self.q: dict[tuple[State, Action], float] = defaultdict(float)  # expected return for given state-action-pair
        self.q_counts: dict[tuple[State, Action], int] = defaultdict(int)

    def determine_action(self, state: State) -> Action:
        action_space = [
            Action(-1, -1),
            Action(0, -1),
            Action(1, -1),
            Action(-1, 0),
            Action(0, 0),
            Action(1, 0),
            Action(-1, 1),
            Action(0, 1),
            Action(1, 1)
        ]

        expected_rewards = np.zeros(len(action_space))
        for i, action in enumerate(action_space):
            expected_rewards[i] = self.q.get((state, action), 0)

        best_action_indices = np.flatnonzero(expected_rewards == np.max(expected_rewards))
        best_action = action_space[random.choice(best_action_indices)]
        return best_action

    def learn(self, episode: list[tuple[State, Action, int]]):
        episode_reversed = list(reversed(episode))
        g = 0
        for i, (state, action, reward) in enumerate(episode_reversed):
            g = self.gamma * g + reward

            is_first_state_action_pair = True
            for _, (state_pre, action_pre, reward_pre) in enumerate(episode_reversed[i + 1::]):
                if state == state_pre and action == action_pre:
                    is_first_state_action_pair = False

            if is_first_state_action_pair:
                n = self.q_counts[(state, action)]
                q = self.q[(state, action)]
                self.q[(state, action)] = (q * n + g) / (n + 1)
                self.q_counts[(state, action)] = n + 1
