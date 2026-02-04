# (Intentionally breaks things)
# Purpose:
# Without anomalies, there is nothing to optimize.
# We inject:
# Approval batching
# Random slowdowns
# Rework loops

import random

class AnomalyInjector:
    def apply(self, step, actor, delay):
        # Manager batching approvals
        if step == "Approved" and actor == "manager":
            if random.random() < 0.4:
                delay *= 3

        # Random rare slowdown
        if random.random() < 0.05:
            delay *= random.randint(2, 4)

        return delay
