from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "Screenshot"
SCREENSHOT_PATH = SCREENSHOT_DIR / "todomvc.png"
URL = "https://demo.playwright.dev/todomvc"

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="chromium")
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
    browser.close()

print(f"Screenshot saved to: {SCREENSHOT_PATH}")
