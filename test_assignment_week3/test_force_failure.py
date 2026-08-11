def test_force_failure(page):
    """Deliberately fail to trigger the screenshot-on-failure fixture."""
    page.goto("https://demo.playwright.dev/todomvc")
    # Force a failure to capture a screenshot
    assert False, "Intentional failure to capture screenshot"
