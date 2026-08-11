import os
import time
import pytest
from playwright.sync_api import sync_playwright


ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Properly capture the test report object so fixtures can inspect pass/fail
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def page(request):
    """Start a Playwright browser page for each test and capture screenshot on failure."""
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    yield page

    # After test: if it failed, capture screenshot
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        name = request.node.name
        ts = int(time.time())
        path = os.path.join(ARTIFACTS_DIR, f"{name}_{ts}.png")
        try:
            page.screenshot(path=path, full_page=True)
            # Print file path for test logs
            print(f"\n[fixture] Saved failure screenshot: {path}")
        except Exception as e:
            print(f"[fixture] Failed to save screenshot: {e}")

    # Cleanup
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
