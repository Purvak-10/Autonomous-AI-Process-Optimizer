# (Simulates people doing work)
# Purpose:
# Assigns actors to steps
# Samples realistic delays
# Calculates cost

import random

class ActorSimulator:
    def __init__(self, company_config):
        self.actors = company_config["actors"]
        self.roles = company_config["roles"]
        self.delays = company_config["delays_minutes"]

    def simulate_step(self, step):
        actor = random.choice(self.actors.get(step, ["system"]))

        delay_range = self.delays.get(step, (1, 5))
        delay = random.randint(delay_range[0], delay_range[1])

        cost_per_minute = self.roles[actor]["cost_per_minute"]
        cost = round(delay * cost_per_minute, 2)

        return actor, delay, cost
