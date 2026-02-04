# (Defines how the AI thinks)
# Purpose:
# Encapsulates expert process-analysis thinking into reusable prompts.

ROOT_CAUSE_PROMPT = """
You are a senior process optimization consultant.

Given the following process metrics and observations:

PROCESS GRAPH EDGES:
{edges}

AVERAGE DURATION PER STEP:
{avg_durations}

DETECTED BOTTLENECKS:
{bottlenecks}

BASELINE METRICS:
{metrics}

Your task:
1. Identify the primary root cause of the main bottleneck.
2. Explain why this bottleneck occurs.
3. Provide evidence from the data.
4. State whether the issue is caused by policy, human behavior, or system design.

Return the result strictly in JSON with keys:
root_cause, explanation, evidence, category
"""
