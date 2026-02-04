import yaml
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def load_company_config():
    path = BASE_DIR / "config" / "company_config.yaml"
    with open(path) as f:
        return yaml.safe_load(f)

def load_sla_rules():
    path = BASE_DIR / "config" / "sla_rules.json"
    with open(path) as f:
        return json.load(f)

def load_scenarios():
    path = BASE_DIR / "config" / "scenarios.yaml"
    with open(path) as f:
        return yaml.safe_load(f)

def get_llm_config():
    return {
        "provider": os.getenv("LLM_PROVIDER"),
        "ollama_model": os.getenv("OLLAMA_MODEL"),
        "openai_key": os.getenv("OPENAI_API_KEY")
    }
