import json
import re
import requests
from src.llm_engine.prompt_registry import ROOT_CAUSE_PROMPT
from src.config_loader import get_llm_config


class ReasoningAgent:
    def __init__(self):
        cfg = get_llm_config()
        self.model = cfg["ollama_model"]
        self.url = "http://localhost:11434/api/generate"
        print(f"[INFO] Using Ollama model: {self.model}")

    def analyze(self, context):
        prompt = ROOT_CAUSE_PROMPT.format(
            edges=context["edges"],
            avg_durations=context["avg_durations"],
            bottlenecks=context["bottlenecks"],
            metrics=context["metrics"]
        )

        print("[INFO] Sending reasoning request to Ollama…")

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        print("[INFO] Response received from Ollama")

        raw_output = response.json().get("response", "").strip()

        print("\n========== RAW MODEL OUTPUT ==========\n")
        print(raw_output)
        print("\n=====================================\n")

        json_str = self._extract_outer_json(raw_output)

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON from LLM output.\n\n"
                f"Extracted JSON:\n{json_str}\n\n"
                f"Full output:\n{raw_output}"
            ) from e

    def _extract_outer_json(self, text: str) -> str:
        """
        Extract the outermost JSON object from LLM output.
        """
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError(f"No JSON object found in LLM output:\n{text}")

        return match.group(0)
