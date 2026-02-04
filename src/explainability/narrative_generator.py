# (Explain decisions in plain English)
# What it does
# Takes final selected policy
# Takes simulation results
# Asks LLM to write a one-paragraph executive summary

import json
import requests
from src.config_loader import get_llm_config

NARRATIVE_PROMPT = """
You are an executive process consultant.

Decision:
{policy}

Simulation Impact:
{impact}

Task:
Write a clear, non-technical explanation (max 6 sentences) answering:
- What problem was found
- What solution was chosen
- Why this solution is better
- What measurable benefits it provides

Avoid technical jargon.
"""

class NarrativeGenerator:
    def __init__(self):
        cfg = get_llm_config()
        self.model = cfg["ollama_model"]
        self.url = "http://localhost:11434/api/generate"

    def generate(self, policy, impact):
        prompt = NARRATIVE_PROMPT.format(
            policy=policy,
            impact=json.dumps(impact, indent=2)
        )

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        return response.json()["response"]
