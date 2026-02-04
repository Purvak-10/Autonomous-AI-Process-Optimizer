import json
import re
import requests
from src.config_loader import get_llm_config

HYPOTHESIS_PROMPT = """
You are a business process optimization expert.

Root Cause:
{root_cause}

Explanation:
{explanation}

Task:
Propose 3 specific, actionable process improvements.

Rules:
- Each proposal must be implementable as a rule
- Each proposal must reduce approval delays
- Avoid illegal or unrealistic changes

Return STRICT JSON in this format:
[
  {{
    "change": "<short_name>",
    "description": "<what is changed>",
    "condition": "<when it applies>",
    "risk": "<low|medium|high>"
  }}
]
"""


class HypothesisGenerator:
    def __init__(self):
        cfg = get_llm_config()
        self.model = cfg["ollama_model"]
        self.url = "http://localhost:11434/api/generate"

    def generate(self, root_cause: str, explanation: str = ""):
        """
        root_cause: normalized string (e.g. 'System Design')
        explanation: optional human-readable explanation
        """

        prompt = HYPOTHESIS_PROMPT.format(
            root_cause=root_cause,
            explanation=explanation or "Approval delays caused by process design."
        )

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        raw_output = response.json().get("response", "").strip()

        print("\n========== RAW MODEL OUTPUT ==========\n")
        print(raw_output)
        print("\n=====================================\n")

        json_str = self._extract_json_array(raw_output)

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse hypothesis JSON.\n\n"
                f"Extracted JSON:\n{json_str}\n\n"
                f"Full output:\n{raw_output}"
            ) from e

    def _extract_json_array(self, text: str) -> str:
        """
        Extract the OUTERMOST JSON array [ ... ] from LLM output.
        """
        match = re.search(r"\[[\s\S]*\]", text)  # 🔥 GREEDY
        if not match:
            raise ValueError(f"No JSON array found in LLM output:\n{text}")

        return match.group(0)
