# (Q-Learning Agent)
# We start with Q-Learning:
# Simple
# Stable
# Interpretable
# Perfect for discrete actions


import random
from collections import defaultdict

class QLearningAgent:
    def __init__(
        self,
        actions,
        alpha=0.1,      # learning rate
        gamma=0.9,      # discount factor
        epsilon=0.2     # exploration rate
    ):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(float)

    def get_state_key(self, state):
        # discretize continuous metrics
        return tuple(round(s, 1) for s in state)

    def choose_action(self, state):
        state_key = self.get_state_key(state)

        # Exploration
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        # Exploitation
        q_values = {
            a: self.q_table[(state_key, a)]
            for a in self.actions
        }
        return max(q_values, key=q_values.get)

    def update(self, state, action, reward, next_state):
        s = self.get_state_key(state)
        ns = self.get_state_key(next_state)

        best_next_q = max(
            self.q_table[(ns, a)] for a in self.actions
        )

        old_q = self.q_table[(s, action)]

        self.q_table[(s, action)] = (
            old_q +
            self.alpha * (reward + self.gamma * best_next_q - old_q)
        )
