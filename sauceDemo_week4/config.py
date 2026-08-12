import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


def _env_bool(key: str, default: str = "true") -> bool:
    value = os.getenv(key, default)
    return str(value).strip().lower() in ("1", "true", "yes", "on")


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    USERNAME = os.getenv("USERNAME", "standard_user")
    PASSWORD = os.getenv("PASSWORD", "secret_sauce")
    BROWSER = os.getenv("BROWSER", "chromium,firefox")
    HEADLESS = _env_bool("HEADLESS", "true")
