import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


def _env_bool(key: str, default: str = "false") -> bool:
    value = os.getenv(key, default)
    return str(value).strip().lower() in ("1", "true", "yes", "on")


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://demo.playwright.dev/todomvc")
    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = _env_bool("HEADLESS", "true")
