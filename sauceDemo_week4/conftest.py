import os
import time
from pathlib import Path

import pytest
from faker import Faker
from playwright.sync_api import sync_playwright

from config import Config

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts" / "screenshots"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def _browser_names():
    values = [name.strip() for name in Config.BROWSER.split(",") if name.strip()]
    return values if values else ["chromium", "firefox"]


@pytest.fixture(params=_browser_names(), ids=lambda value: value)
def browser_name(request):
    return request.param


@pytest.fixture(scope="session")
def faker():
    return Faker()


@pytest.fixture
def random_invalid_credentials(faker):
    return {
        "username": faker.user_name(),
        "password": faker.password(length=12),
    }


@pytest.fixture
def page(request, browser_name):
    headed = request.config.getoption("--headed")
    headless = False if headed else Config.HEADLESS

    playwright = sync_playwright().start()
    browser_type = getattr(playwright, browser_name)
    browser = browser_type.launch(headless=headless, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    yield page

    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        test_name = request.node.name
        timestamp = int(time.time())
        screenshot_path = ARTIFACTS_DIR / f"{test_name}_{browser_name}_{timestamp}.png"
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"\n[fixture] Saved failure screenshot: {screenshot_path}")
        except Exception as exc:
            print(f"[fixture] Unable to capture screenshot: {exc}")

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
        playwright.stop()
    except Exception:
        pass


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run Playwright tests in headed mode.",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)
