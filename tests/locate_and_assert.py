from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
URL = "https://demo.playwright.dev/todomvc"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(URL, wait_until="networkidle", timeout=60000)

        # Five different locator strategies:
        locators = {
            "css_selector (input.new-todo)": page.locator("input.new-todo"),
            "placeholder (What needs to be done?)": page.get_by_placeholder("What needs to be done?"),
            "role (heading name=\"todos\")": page.get_by_role("heading", name="todos"),
            "text (Double-click to edit a todo)": page.get_by_text("Double-click to edit a todo"),
            "xpath (footer)": page.locator("xpath=//footer"),
        }

        # Assert visibility for each locator
        failures = []
        for desc, loc in locators.items():
            try:
                # wait_for ensures the element becomes visible within the timeout
                loc.first.wait_for(state="visible", timeout=5000)
                print(f"OK: {desc} is visible")
            except Exception as e:
                failures.append((desc, str(e)))

        browser.close()

        if failures:
            msg_lines = [f"{d}: {err}" for d, err in failures]
            raise AssertionError("Some locators were not visible:\n" + "\n".join(msg_lines))


if __name__ == "__main__":
    main()
