# (Find where time is lost)
# What is a bottleneck?
# A step or transition that takes much longer than others
# Or occurs too frequently in loops
# We detect bottlenecks using average duration per step.


from collections import defaultdict
import statistics

class BottleneckDetector:
    def __init__(self, traces):
        self.traces = traces

    def detect(self):
        step_durations = defaultdict(list)

        for events in self.traces.values():
            for event in events:
                step_durations[event["step"]].append(event["duration"])

        avg_durations = {
            step: statistics.mean(durations)
            for step, durations in step_durations.items()
        }

        overall_avg = statistics.mean(avg_durations.values())

        bottlenecks = {
            step: avg
            for step, avg in avg_durations.items()
            if avg > overall_avg * 1.3  # threshold
        }

        return bottlenecks, avg_durations


