# (Builds LLM-safe context)
# Purpose:
# LLMs cannot ingest massive datasets.
# This module:
# Extracts only what matters
# Formats it cleanly
# Prevents hallucinations


class ContextBuilder:
    def build(
        self,
        graph_edges,
        avg_durations,
        bottlenecks,
        metrics
    ):
        return {
            "edges": graph_edges,
            "avg_durations": avg_durations,
            "bottlenecks": bottlenecks,
            "metrics": metrics
        }
