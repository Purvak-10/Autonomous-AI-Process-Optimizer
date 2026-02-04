# (Build the real workflow graph)
# What this does
# Nodes = steps (Created, Assigned, etc.)
# Edges = transitions
# Edge weight = frequency of transition
# This shows how work actually flows, not how we think it flows.



import networkx as nx

class ProcessGraphBuilder:
    def __init__(self, traces):
        self.traces = traces
        self.graph = nx.DiGraph()

    def build(self):
        for case_id, events in self.traces.items():
            for i in range(len(events) - 1):
                src = events[i]["step"]
                dst = events[i + 1]["step"]

                if self.graph.has_edge(src, dst):
                    self.graph[src][dst]["count"] += 1
                else:
                    self.graph.add_edge(src, dst, count=1)

        return self.graph
