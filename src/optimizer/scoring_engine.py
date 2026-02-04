# (The brain of decision-making)
# What this does
# Accepts simulation deltas
# Applies weights
# Produces a single scalar score
# Ranks policies

class ScoringEngine:
    def __init__(
        self,
        w_cycle_time=0.5,
        w_cost=0.3,
        w_sla=0.2
    ):
        self.w_cycle_time = w_cycle_time
        self.w_cost = w_cost
        self.w_sla = w_sla

    def score(self, delta_metrics):
        """
        delta_metrics example:
        {
          'avg_cycle_time': -272.2,
          'avg_cost': -165.0,
          'sla_violation_rate': -0.265
        }
        """

        score = (
            self.w_cycle_time * (-delta_metrics["avg_cycle_time"]) +
            self.w_cost * (-delta_metrics["avg_cost"]) +
            self.w_sla * (-delta_metrics["sla_violation_rate"] * 100)
        )

        return round(score, 2)

    def rank(self, simulation_results):
        """
        simulation_results:
        {
          rule_name: {
            "baseline": {...},
            "experimental": {...},
            "delta": {...}
          }
        }
        """

        ranking = []

        for rule, results in simulation_results.items():
            s = self.score(results["delta"])
            ranking.append({
                "rule": rule,
                "score": s,
                "delta": results["delta"]
            })

        ranking.sort(key=lambda x: x["score"], reverse=True)
        return ranking
