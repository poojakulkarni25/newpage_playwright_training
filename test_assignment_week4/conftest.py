import json
import os
import time
from pathlib import Path

import pytest
from faker import Faker
from playwright.sync_api import sync_playwright

from .config import Config

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


@pytest.fixture(params=["chromium", "firefox"], ids=["chromium", "firefox"])
def browser_name(request):
    return request.param


@pytest.fixture
def dynamic_todo_items():
    fake = Faker()
    verbs = ["Buy", "Call", "Write", "Review", "Fix", "Submit", "Schedule", "Clean", "Organize", "Plan"]
    objects = [
        "groceries",
        "emails",
        "the report",
        "the presentation",
        "the meeting",
        "the invoice",
        "the code",
        "the schedule",
        "the project",
        "the budget",
    ]
    return [
        f"{fake.random_element(verbs)} {fake.random_element(objects)}"
        for _ in range(5)
    ]


@pytest.fixture
def static_todo_data():
    fixture_path = Path(__file__).resolve().parent / "fixtures" / "todo_data.json"
    with fixture_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run Playwright tests in headed mode (visible browser).",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def page(request, browser_name):
    headed = request.config.getoption("--headed")
    headless = False if headed else Config.HEADLESS

    pw = sync_playwright().start()
    browser_type = getattr(pw, browser_name)
    browser = browser_type.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()

    yield page

    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        name = request.node.name
        ts = int(time.time())
        browser_name = request.getfixturevalue("browser_name")
        path = os.path.join(ARTIFACTS_DIR, f"{name}_{browser_name}_{ts}.png")
        try:
            page.screenshot(path=path, full_page=True)
            print(f"\n[fixture] Saved failure screenshot: {path}")
        except Exception as exc:
            print(f"[fixture] Failed to save screenshot: {exc}")

    try:
        page.close()
    except Exception:
        pass
    try:
        context.close()
    except Exception:
        pass
    try:
        browser.close()
    except Exception:
        pass
    try:
        pw.stop()
    except Exception:
        pass
