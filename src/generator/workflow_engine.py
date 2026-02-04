# (Controls process flow)
# Purpose:
# Reads workflow & transitions from config
# Decides the next step probabilistically


import random

ticket_value = random.randint(100, 5000)

class WorkflowEngine:
    def __init__(self, config):
        self.transitions = config["transitions"]

    def get_next_step(self, current_step):
        if current_step not in self.transitions:
            return None

        next_steps = self.transitions[current_step]
        steps = list(next_steps.keys())
        probs = list(next_steps.values())

        return random.choices(steps, probs)[0]
