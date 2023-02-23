from state import State
from action import Action
from collections import defaultdict
import numpy as np
from random import Random


class ModelRLMC:
    def __init__(self, random_state: int | None):
        self.rnd = Random(random_state)
        self.gamma = 0.9
        self.epsilon = 0.1

        self.q: dict[tuple[State, Action], float] = defaultdict(float)  # expected return for given state-action-pair
        self.q_counts: dict[tuple[State, Action], int] = defaultdict(int)

        self.action_space = [
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

    def determine_epsilon_action(self, state: State) -> Action:
        if self.rnd.random() < 1-self.epsilon:
            return self.determine_best_action(state)
        else:
            return Action(0, 0)

    def determine_rnd_action(self) -> Action:
        return self.rnd.choice(self.action_space)

    def determine_best_action(self, state: State) -> Action:
        # calc expected rewards foreach action
        expected_rewards = np.zeros(len(self.action_space))
        for i, action in enumerate(self.action_space):
            expected_rewards[i] = self.q.get((state, action), 0)
        # select action with the highest expected reward
        best_action_indices = np.flatnonzero(expected_rewards == np.max(expected_rewards))
        best_action_index = self.rnd.choice(best_action_indices)
        return self.action_space[best_action_index]

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
